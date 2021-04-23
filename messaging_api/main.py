import datetime
import asyncio
from asgiref.sync import sync_to_async

from fastapi import FastAPI, Request, status, Response, Depends
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse
from django.http.response import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from typing import Optional, List
from account.models import UserInfo
from messaging.models import Chat, Message
from .schemas import ChatModel, MessageAnswerModel, UserModel, MessageModel, UserBaseModel
from sse_starlette.sse import EventSourceResponse
from dependencies import csrf_depend
from dependencies import queue_manager as qmanager

import json

app = FastAPI()

@app.get("/get_chats", response_class=JSONResponse, response_model=UserModel, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}})
def get_chats(request: Request, response: Response, valid_csrf: bool = Depends(csrf_depend)):
    user = request.state.user
    if (isinstance(user, AnonymousUser)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    #if not valid_csrf:
    #    response.status_code = status.HTTP_403_FORBIDDEN
    #    return JSONResponse({"error": "Invalid CSRFToken"})
    chats = user.chats.all()
    chat_list = []
    for chat in chats:
        user_list = []
        users = chat.users.all()
        for user_ in users:
            if user_.id == user.id:
                continue
            user_list.append(user_)
        
        if len(user_list) == 1: # Если личный чат
            chat_model_dict = {}
            chat_model_dict["name"] = user_list[0].username
            chat_model_dict["icon"] = user_list[0].userinfo.img.url
            chat_model_dict["link"] = reverse("messaging:chat") + f"?chatid={chat.id}"
            try:
                last_message = chat.messages.all().order_by("-created")[0]
            except IndexError:  # TODO Сделать часовые пояса
                chat_model_dict["last_message"] = ""
                chat_model_dict["date"] = datetime.datetime.fromtimestamp(0)
                chat_model_dict["lm_date"] = ""
            else:
                chat_model_dict["last_message"] = last_message.text
                chat_model_dict["date"] = last_message.created
                chat_model_dict["lm_date"] = (last_message.created + datetime.timedelta(hours=3)).strftime("%I:%M %p")
                    
        else:                   # Если групповой чат
            raise ValueError("Групповой чат не реализован")
        print(chat_model_dict)

        chat_list.append(ChatModel(**chat_model_dict))

    user_model_dict = {}
    user_model_dict["name"] = user.username
    user_model_dict["link"] = reverse("account:cabinet")
    user_model_dict["icon"] = user.userinfo.img.url
    user_model_dict["chats"] = chat_list
    return UserModel(**user_model_dict)


@app.get("/get_pr_message", response_class=JSONResponse, response_model=MessageAnswerModel, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}})
async def get_pr_messages(request: Request, response: Response, chatid: int, limit: int = Query(default=50), offset: int = Query(default=0), last_date: Optional[datetime.datetime] = Query(None)):#, valid_csrf: bool = Depends(csrf_depend)):
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    #if not valid_csrf:
    #    response.status_code = status.HTTP_403_FORBIDDEN
    #    return JSONResponse({"error": "Invalid CSRFToken"})
    
    user = request.state.user
    try:
        get_chat = sync_to_async(Chat.objects.get)
        chat = await get_chat(id=chatid)
    except Chat.DoesNotExist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse({"error": "Chat with this id does not exist"})
    user_exists = sync_to_async(chat.users.filter(id=user.id).exists)
    if not await user_exists():
        response.status_code = status.HTTP_403_FORBIDDEN
        return JSONResponse({"error": "This user does not own this chat"})

    if last_date:
        filter_messages = sync_to_async(chat.messages.filter(created__gt=last_date).order_by("created").all)
        messages = await filter_messages()
    else:
        offset_messages = sync_to_async(chat.messages.order_by("-created")[offset:offset + limit + 1].all)
        messages = await offset_messages()

    get_all_users = sync_to_async(chat.users.all)
    to_list = sync_to_async(list)
    users = await to_list(await get_all_users())
    users.remove(user)
    user1 = users[0]

    @sync_to_async
    def check_messages():
        checked_messages = []
        for message in messages:
            if not message.is_checked and message.user.id == user1.id:
                checked_messages.append(message.id)
                message.is_checked = True
                message.save()
        return checked_messages

    checked_messages = await check_messages()
    try:
        await qmanager.put_to_queue(user.id, object={"event": "checked_message", "data": json.dumps(checked_messages)})
    except ValueError:
        pass

    try:
        await qmanager.put_to_queue(user1.id, object={"event": "checked_message", "data": json.dumps(checked_messages)})
    except ValueError:
        pass
    
    @sync_to_async
    def get_messageanswermodel():
        _messages = [MessageModel(date=mes.created, text=mes.text, author=mes.user.username, is_checked=mes.is_checked, id=mes.id) for mes in messages]
        sender = UserBaseModel(name=user.username, icon=user.userinfo.img.url, link=f"{reverse('account:cabinet')}?userid={user.id}")
        users = list(chat.users.all())
        users.remove(user)
        user1 = users[0]
        reciever = UserBaseModel(name=user1.username, icon=user1.userinfo.img.url, link=f"{reverse('account:cabinet')}?userid={user1.id}")
        return MessageAnswerModel(sender=sender, reciever=reciever, chat_story=list(reversed(_messages)))
    return await get_messageanswermodel()


@app.post("/send_pr_message", response_class=JSONResponse, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}}, status_code=status.HTTP_201_CREATED)
async def send_pr_message(request: Request, response: Response, chatid: int, item: MessageModel): #, valid_csrf: bool = Depends(csrf_depend))
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    #if not valid_csrf:
    #    response.status_code = status.HTTP_403_FORBIDDEN
    #    return JSONResponse({"error": "Invalid CSRFToken"})
    user = request.state.user
    try:
        get_chat = sync_to_async(Chat.objects.get)
        chat = await get_chat(id=chatid)
    except Chat.DoesNotExist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse({"error": "Chat with this id does not exist"})

    get_all_users = sync_to_async(chat.users.all)
    user_exists = sync_to_async(chat.users.filter(id=user.id).exists)
    if not await user_exists():
        response.status_code = status.HTTP_403_FORBIDDEN
        return JSONResponse({"error": "This user does not own this chat"})
    new_message = sync_to_async(Message)
    message = await new_message(text=item.text, user=user, chat=chat)
    save_func = sync_to_async(message.save)
    await save_func()
    users = await get_all_users()
    to_list = sync_to_async(list)
    users = await to_list(users)
    users.remove(user)
    user1 = users[0]

    try:
        await qmanager.put_to_queue(user1.id, object={"event": "got_message", "data": ""})
    except ValueError:
        pass
    try:
        await qmanager.put_to_queue(user.id, object={"event": "got_message", "data": ""})
    except ValueError:
        pass

    response.status_code = status.HTTP_201_CREATED
    return JsonResponse({"message": "created"})


@app.get("/chat_events", response_class=EventSourceResponse)
async def chat_events(request: Request, response: Response): #, valid_csrf: bool = Depends(csrf_depend))
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    #if not valid_csrf:
    #    response.status_code = status.HTTP_403_FORBIDDEN
    #    return JSONResponse({"error": "Invalid CSRFToken"})
    user = request.state.user
    async def event_publisher():
        user_str = user.id
        try:
            uid = qmanager.create_queue(user_str)
        except ValueError:
            pass
        try:
            while True:
                disconnected = await request.is_disconnected()
                if disconnected:
                    print(f"Disconnecting client {request.client}")
                    break
                event = await qmanager.get_from_queue(user_str, uid)
                if event is None:
                    continue
                yield event
            print(f"Disconnected from client {request.client}")
        except asyncio.CancelledError as e:
          print(f"Disconnected from client (via refresh/close) {request.client}")
          # Do any other cleanup, if any
          raise e
        finally:
            qmanager.del_queue(user_str, uid)
    
    return EventSourceResponse(event_publisher())

from django.contrib.auth.models import AnonymousUser, User
from account.models import Post
from fastapi import FastAPI, Request, status, Response, Query, Depends
from fastapi.responses import JSONResponse
import asyncio
from asgiref.sync import sync_to_async
from .constants import TRANSLATIONS
from .schemas import *
from dependencies import csrf_depend
from typing import Dict


app = FastAPI()


@app.get("/get_info", response_class=JSONResponse, response_model=AccountInfoModel, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}})
def get_info(request: Request, response: Response, userid: Optional[str] = Query(None), valid_csrf: bool = Depends(csrf_depend)):
    if not valid_csrf:
        response.status_code = status.HTTP_403_FORBIDDEN
        return JSONResponse({"error": "Invalid CSRFToken"})
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})

    if userid is None:
        user = request.state.user
        is_owner = True
    else:
        try:
            userid = int(userid)
            user = User.objects.get(pk=userid)
            is_owner = userid == request.state.user.id
        except ValueError:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return JSONResponse({"error": "userid query must be a number"})
        except User.DoesNotExist:
            response.status_code = status.HTTP_403_FORBIDDEN
            return JSONResponse({"error": "User with this id does not exist"})
    username = user.username
    age = user.userinfo.age
    genres = list(user.userinfo.genres.all())
    instruments = list(user.userinfo.instruments.all())
    favourite_bands = list(user.userinfo.favourite_bands)
    songs = list(user.userinfo.songs)
    img = user.userinfo.img.url
    db_posts = user.posts.all()
    link = f"/account/cabinet?userid={user.id}"
    posts = [PostModel(date=post.created, message=post.message, audio=(post.audio.url if post.audio else None)) for post in db_posts]
    return AccountInfoModel(name=username, genre=list(
            map(lambda x: TRANSLATIONS[x.name], genres)
        ), 
        age=age, 
        instruments=list(map(lambda x: TRANSLATIONS[x.name], instruments)),
        posts=posts, 
        img=img, 
        favourite_bands=favourite_bands, 
        songs=songs,
        is_owner=is_owner,
        link=link
    )


@app.post("/create_post", response_class=JSONResponse, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}}, status_code=status.HTTP_201_CREATED)
def create_post(request: Request, response: Response, item: PostInputModel, valid_csrf: bool = Depends(csrf_depend)):
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    if not valid_csrf:
        response.status_code = status.HTTP_403_FORBIDDEN
        return JSONResponse({"error": "Invalid CSRFToken"})

    post = Post(message=item.message, audio=item.audio, user=request.state.user)
    post.save()
    response.status_code = status.HTTP_201_CREATED
    return JSONResponse({"message": "created"})

@sync_to_async
def async_get_userstatus(userid):
    return User.objects.get(id=userid).userstatus

class OnlineAwaiter:
    def __init__(self):
        self._usrs: Dict[asyncio.Task] = dict()


    async def _become_offline(self, userid:int):
        await asyncio.sleep(30)
        userstatus = await async_get_userstatus(userid)
        userstatus.is_online = False
        async_save = sync_to_async(userstatus.save)
        await async_save()
        del self._usrs[userid]
        print("offline")


    async def stay_online(self, userid:int):
        if self._usrs.get(userid, None) is None:
            self._usrs[userid] = asyncio.create_task(self._become_offline(userid))
            
            task: asyncio.Task = self._usrs[userid]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                del task
                self._usrs[userid] = asyncio.create_task(self._become_offline(userid))
        


online_awaiter = OnlineAwaiter()
        

@app.get("/remain_online", response_class=JSONResponse, responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_403_FORBIDDEN: {"description": "Forbidden", "content": {"application/json": {"example": {"error": "Description of an error"}}}}, status.HTTP_400_BAD_REQUEST: {"description": "Bad request", "content": {"application/json": {"example": {"error": "Description of an error"}}}}}, status_code=status.HTTP_202_ACCEPTED)
async def remain_online(request: Request, response: Response):#, valid_csrf: bool = Depends(csrf_depend)):
    if isinstance(request.state.user, AnonymousUser):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse({"error": "Unauthorized user is trying to use API"})
    #if not valid_csrf:
    #    response.status_code = status.HTTP_403_FORBIDDEN
    #    return JSONResponse({"error": "Invalid CSRFToken"})
    userstatus = await async_get_userstatus(request.state.user.id)
    if userstatus.is_online == False:
        userstatus.is_online = True
        async_save = sync_to_async(userstatus.save)
        await async_save()
    asyncio.create_task(online_awaiter.stay_online(request.state.user.id))
    response.status_code = status.HTTP_202_ACCEPTED
    return JSONResponse({"message": "accepted"})

from typing import Dict, Optional
import uuid
import asyncio
from asgiref.sync import sync_to_async
from fastapi import Request, Cookie, Header
from starlette.middleware.base import BaseHTTPMiddleware
from importlib import import_module
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.middleware.csrf import CSRF_SECRET_LENGTH, CSRF_ALLOWED_CHARS

_django_session_engine = import_module(settings.SESSION_ENGINE)


class QueueManager:
    def __init__(self):
        self._qdct: Dict[str, Dict[str, asyncio.Queue]] = {}
    

    def create_queue(self, user: int):
        dct = self._qdct.setdefault(user, {})
        uid = uuid.uuid4()
        dct.setdefault(uid, asyncio.Queue())
        return uid


    async def get_from_queue(self, user: int, uid:uuid.UUID):
        usr = self._qdct.get(user, None)
        if usr is None:
            raise ValueError("There are not queues assigned to this user")
        queue = usr.get(uid, None)
        if queue is None:
            raise ValueError("There are not queues with this uuid on this user")
        try:
            item = await asyncio.wait_for(queue.get(), timeout=5)
        except asyncio.TimeoutError:
            return
        return item

    
    async def put_to_queue(self, user: int, uid: Optional[uuid.UUID]=None, *, object):
        usr = self._qdct.get(user, None)
        if usr is None:
            raise ValueError("There are not queues assigned to this user")
        if uid:
            queue = usr.get(uid, None)
            if queue is None:
                raise ValueError("There are not queues with this uuid on this user")
            await queue.put(object)
        else:
            for q in usr.values():
                await q.put(object)


    def del_queue(self, user:int, uid: uuid.UUID):
        usr = self._qdct.get(user, None)
        if usr is None:
            raise ValueError("There are not queues assigned to this user")
        queue = usr.get(uid, None)
        if queue is None:
            raise ValueError("There are not queues with this uuid on this user")
        del usr[uid]
        if len(usr) == 0:
            del self._qdct[user]


async def get_user_from_session(sessionid: Optional[str] = None):
    if sessionid is None:
        return AnonymousUser()
    else:
        session = _django_session_engine.SessionStore(sessionid)
        async_session_get = sync_to_async(session.get)
        uid = await async_session_get('_auth_user_id')
        if uid is None:
            return AnonymousUser()
        else:
            async_user_get = sync_to_async(User.objects.get)
            try:
                user: User = await async_user_get(id=uid)
                return user
            except User.DoesNotExist:
                return AnonymousUser()


async def user_depend(sessionid: Optional[str] = Cookie(None)):
    return await get_user_from_session(sessionid)


class DjangoUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        sessionid = request.cookies.get("sessionid", None)
        user = await get_user_from_session(sessionid)
        request.state.user = user
        response = await call_next(request)
        return response


def _unsalt_token(token):
    salt = token[:CSRF_SECRET_LENGTH]
    token = token[CSRF_SECRET_LENGTH:]
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in token), (chars.index(x) for x in salt))
    secret = ''.join(chars[x - y] for x, y in pairs)  # Note negative values are ok
    return secret


def csrf_depend(X_CSRFToken: Optional[str] = Header(None), csrftoken: Optional[str] = Cookie(str)):
    if X_CSRFToken is None or csrftoken is None:
        return False
    return _unsalt_token(X_CSRFToken) == _unsalt_token(csrftoken)

queue_manager = QueueManager()
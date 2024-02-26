'''some description'''
import logging
import sys
from datetime import timedelta
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from couchdb import Server
import redis
from core.settings import SettingsJWT
##########################

from dependencies.jwt import \
    create_access_token, get_current_user, validate_user
from dependencies.get_db import get_dbusr
from controllers.save_message import \
    save_message_user, get_message_login, validate_request
from helper.api import generate_api_key, generate_secret_word
from helper.db_delete_docs import delete_docs_except_design_views
from models.model import MessageGeneralSchema, MessageResponseSchema, \
    MessageSchema, UserApiCreate, UserLoginSchema
from models.classes import UserClass, UserPwdClass

sys.path.insert(0, '/code/fastapis/dependencies')
sys.path.insert(1, '/code/fastapis/controllers')
sys.path.insert(2, '/code/fastapis/models')

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={404: {"description": "Not found"}}
)


@router.get("/health")
def health():
    '''method description'''
    logger = logging.getLogger('global_logger')
    logger.info("Called 'health'", extra={
                'username': 'xxxxxxxxx', 'merchant': 'yyyyyyyy'})
    return {"messages_is_alive": True}


@router.post("/user/signup", tags=["user"])
async def create_user(
    user: UserPwdClass,
    current_user: UserClass = Depends(get_current_user),
    dbu: Server = Depends(get_dbusr)
) -> UserPwdClass:
    '''method description'''
    # current_user: UserClass = await get_current_user(user.token)

    user = await save_message_user(
        dbu=dbu,
        new=user,
        tokenusr=current_user)

    # response = MessageUser()
    # user.id = doc_id
    return user


@router.post("/user/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    '''JWT Login For Access Token'''
    settings = SettingsJWT()
    user: UserClass = validate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt_expires)
    access_token = create_access_token(
        data=user.to_dict(),
        expires_delta=access_token_expires
    )
    user.token = access_token
    return user


@router.get("/user/me")
async def read_users_me(current_user: UserClass = Depends(get_current_user)):
    '''JWT get Current User'''
    return current_user


@router.post("/user/login", tags=["user"])
async def user_login(
    user: UserLoginSchema,
    db: Server = Depends(get_dbusr)
) -> MessageSchema:
    '''description'''

    response = get_message_login(db, user)

    return response


@router.post("/user/createapi", tags=["user"])
async def user_create_api(
    o_api: UserApiCreate,
    current_user: UserClass = Depends(get_current_user),
    dbu: Server = Depends(get_dbusr)
) -> UserApiCreate:
    '''Create user api credentials'''
    doc = dbu.get(o_api.id)
    ok: bool = await validate_request(tokenusr=current_user, udoc=doc)

    if ok:
        doc["apitoken"] = generate_api_key()
        doc["apisecret"] = generate_secret_word()
        o_api.apitoken = doc["apitoken"]
        o_api.apisecret = doc["apisecret"]

        dbu.save(doc)

    delattr(o_api, "token")
    return o_api


@router.post("/users", tags=["user"])
async def get_users(
    request: MessageGeneralSchema,
    db_usr: Server = Depends(get_dbusr)
) -> List[UserClass]:
    '''get all active users'''

    o_user: UserClass = UserClass(**db_usr.get(request.username))
    queried_documents: List[UserClass] = []
    if o_user.active:
        if o_user.active and o_user.merchant == "*":
            view_result = db_usr.view(
                'Users/vUsers',
                include_docs=False)
        else:
            view_result = db_usr.view(
                'Users/vUsers',
                key=[o_user.merchant, True],
                include_docs=False)

        # Extract documents from the view result
        queried_documents = [UserClass(**row.value) for row in view_result]

    return queried_documents


@router.post("/user/delete", tags=["user"])
async def delete_user(
    request: MessageGeneralSchema,
    dbu: Server = Depends(get_dbusr)
) -> MessageResponseSchema:
    '''get all active users'''

    o_user: UserClass = UserClass(**dbu.get(request.username))
    doc = dbu.get(request.message)
    if doc and o_user.active \
            and (
                o_user.role == "owner"
                or (
                    o_user.role == "admin"
                    and o_user.merchant == doc["merchant"]
                )
            ) \
            and doc["username"] != request.username:
        dbu.delete(doc)

        response: MessageResponseSchema = \
            MessageResponseSchema(message="deleted", error=None)
    else:
        response: MessageResponseSchema = \
            MessageResponseSchema(message="nok",
                                  error="deletion is not valid")
    return response


@router.post("/user/activate_deactivate", tags=["user"])
async def user_activate_deactivate(
    request: MessageGeneralSchema,
    dbu: Server = Depends(get_dbusr)
) -> UserClass:
    '''get all active users'''

    o_user: UserClass = UserClass(**dbu.get(request.username))
    doc = dbu.get(request.message)
    if doc and o_user.active \
            and (
                o_user.role == "owner"
                or (
                    o_user.role == "admin"
                    and o_user.merchant == doc["merchant"]
                )
            ) \
            and doc["username"] != request.username:
        if doc["active"]:
            doc["active"] = False
        else:
            doc["active"] = True
        dbu.save(doc)

        doc["message"] = "ok"
    else:
        doc["message"] = "nok"
    return doc


@router.delete("/delete_docs/{db_name}")
async def delete_docs(db_name: str):
    '''endpoint to delete database documents'''
    success, message = delete_docs_except_design_views(db_name)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}


redis_client = redis.Redis(host='10.5.0.4', port=6379, db=0)


@router.get("/counter")
def counter_next(countid: str) -> int:
    '''Counter increment'''
    # Increment and retrieve the counter value
    counter_value = redis_client.incr(countid)
    if counter_value > 1000000000:
        redis_client.set(countid, 0)
    return int(counter_value)


@router.get("/counterleading0")
def counter_next_leading_0(countid: str) -> str:
    '''Counter increment with leading 0s'''
    # Increment and retrieve the counter value
    counter_value = counter_next(countid)
    return str(counter_value).zfill(10)

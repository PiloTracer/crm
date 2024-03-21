'''JWT management'''
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.settings import SettingsJWT

from dependencies import get_db
from models.classes import UserClass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="messages/user/token")

settings = SettingsJWT()
dbu = get_db.get_dbusr()


def validate_user(username: str, password: str) -> Optional[UserClass]:
    '''JWT User validation'''
    retrieved = dbu.get(username.lower())
    myuser = UserClass()
    try:
        if retrieved \
                and retrieved['password'] == password \
                and retrieved['active']:
            # myuser = UserClass(**retrieved)
            myuser = UserClass(**retrieved)
            myuser.msg = "The credentials are valid"
        else:
            myuser.msg = "Wrong credentials"
            myuser.err = "ERR: login failed"
    except Exception as e:  # pylint: disable=broad-except
        myuser.err = e
    return myuser


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''JWT Create Access Token'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expires)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) \
        -> Optional[UserClass]:
    '''JWT Get Current User'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_algorithm])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = payload  # token data contains all user info
    except JWTError as exc:
        raise credentials_exception from exc
    user = UserClass(**token_data)
    return user

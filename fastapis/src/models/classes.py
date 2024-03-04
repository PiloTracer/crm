"""Module providing a class to parse data."""
import time
from typing import Optional
from pydantic import BaseModel, Field

from models.model import UserApiCreate


class RabbitMessage(BaseModel):
    """Class for rabbitmq messaging"""
    type: str = None
    channel: str = None
    header: str = None
    message: str = None
    merchant: str = None
    wstoken: str = None

    def to_dict(self):
        """convert to dict"""
        return {
            'type': self.type,
            'channel': self.channel,
            'header': self.header,
            'message': self.message,
            'merchant': self.merchant
        }

    # def to_str(self):
    #    """convert to string"""
    #    return "{'type':'" + self.type \
    #        + "', 'channel':'" + self.channel \
    #        + "', 'header':'" + self.header \
    #        + "', 'message':'" + self.message + "' }"


class UserClass(BaseModel):
    """Class representing a class of a User"""
    # {'id': doc._id, 'role': doc.role, 'fullname': doc.fullname,
    # 'username': doc.username, 'merchant':
    # doc.merchant, 'active': doc.active});
    id: str = Field(None, alias='_id')
    type: Optional[str] = None
    role: Optional[str] = None
    fullname: Optional[str] = None
    username: Optional[str] = None
    msg: Optional[str] = None
    err: Optional[str] = None
    merchant: Optional[str] = None
    active: Optional[bool] = False
    message: Optional[str] = None
    createds: float = Field(default_factory=time.time)
    modifieds: float = Field(default_factory=time.time)
    created_by: Optional[str] = None
    created_merchant: Optional[str] = None
    token: Optional[str] = None

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            '_id': self.id,
            'type': self.type,
            'role': self.role,
            'fullname': self.fullname,
            'username': self.username,
            'msg': self.msg,
            'err': self.err,
            'merchant': self.merchant,
            'active': self.active,
            'message': self.message,
            'createds': self.createds,
            'modifieds': self.modifieds,
            'created_by': self.created_by,
            'created_merchant': self.created_merchant,
            'token': self.token
        }

    @classmethod
    def from_dict(cls, data):
        """parse"""
        # Create an object from a dictionary retrieved from CouchDB
        return cls(
            id=data.id,
            type=data.get('type'),
            role=data.get('role'),
            fullname=data.get('fullname'),
            username=data.get('username'),
            merchant=data.get('merchant'),
            active=data.get('active'),
            message=data.get('message'),
            createds=data.get('createds'),
            modifieds=data.get('modifieds'),
            created_by=data.get('created_by'),
            created_merchant=data.get('created_merchant')
        )


class UserPwdClass(UserClass):
    """Class representing a class of a User"""
    password: str = None

    def get_user_api_create(self) -> UserApiCreate:
        '''get a UserApiCreate object for validation'''
        obj = UserApiCreate(id=self.id,
                            merchant=self.merchant)
        return obj

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            '_id': self.id,
            'type': self.type,
            'role': self.role,
            'fullname': self.fullname,
            'username': self.username,
            'merchant': self.merchant,
            'password': self.password,
            'active': self.active,
            'message': self.message,
            'createds': self.createds,
            'modifieds': self.modifieds,
            'created_by': self.created_by,
            'created_merchant': self.created_merchant
        }

    @classmethod
    def from_dict(cls, data):
        """parse"""
        # Create an object from a dictionary retrieved from CouchDB
        return cls(
            id=data.get('_id'),
            type=data.get('type'),
            role=data.get('role'),
            fullname=data.get('fullname'),
            username=data.get('username'),
            merchant=data.get('merchant'),
            password=data.get('password'),
            active=data.get('active'),
            message=data.get('message'),
            createds=data.get('createds'),
            modifieds=data.get('modifieds'),
            created_by=data.get('created_by'),
            created_merchant=data.get('created_merchant')
        )


class UserApiClass(UserClass):
    """Class representing a class of a User"""
    apitoken: Optional[str] = None
    apisecret: Optional[str] = None

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            '_id': self.id,
            'type': self.type,
            'role': self.role,
            'fullname': self.fullname,
            'username': self.username,
            'merchant': self.merchant,
            'password': self.password,
            'active': self.active,
            'message': self.message,
            'createds': self.createds,
            'created_by': self.created_by,
            'created_merchant': self.created_merchant,
            'apitoken': self.apitoken,
            'apisecret': self.apisecret
        }

    @classmethod
    def from_dict(cls, data):
        """parse"""
        # Create an object from a dictionary retrieved from CouchDB
        return cls(
            id=data.get('_id'),
            type=data.get('type'),
            role=data.get('role'),
            fullname=data.get('fullname'),
            username=data.get('username'),
            merchant=data.get('merchant'),
            password=data.get('password'),
            active=data.get('active'),
            message=data.get('message'),
            createds=data.get('createds'),
            created_by=data.get('created_by'),
            created_merchant=data.get('created_merchant'),
            apitoken=data.get('apitoken'),
            apisecret=data.get('apisecret')
        )

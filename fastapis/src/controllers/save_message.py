""" just a description """
import time
from couchdb import Server
from models.model import UserLoginSchema, MessageUser
from models.classes import UserClass, UserPwdClass


async def save_message_user(dbu: Server,
                            new: UserPwdClass,
                            tokenusr: UserClass,
                            src: str) -> MessageUser:
    """Save a user message to the database."""
    new.id = f'{new.username.lower()}'
    new.type = "user"
    new.createds = time.time()
    ok = src == "direct"

    if ok is False:
        doc = dbu.get(new.created_by)
        ok = await validate_request(
            tokenusr=tokenusr,
            udoc=doc)

    if ok:
        # pylint: disable=unused-variable
        doc_id, doc_rev = dbu.save(
            new.to_dict())
        new.id = doc_id
        new.password = ""
        new.message = "ok"

    return new


async def validate_request(tokenusr: UserClass, udoc: any) -> bool:
    '''Validates a request token'''
    return (udoc is not None
            and tokenusr.merchant == udoc["merchant"]
            and udoc["active"]
            and ((udoc["merchant"] == "*" and udoc["role"] == "owner")
                 or (udoc["role"] == "admin"))
            )


def get_message_login(db: Server, user: UserLoginSchema) -> UserClass:
    """
    Validate User.
    """
    retrieved = db.get(user.username.lower())
    myuser = UserClass()
    try:
        if retrieved and retrieved['password'] == user.password \
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

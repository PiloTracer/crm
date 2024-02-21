'''this is a description'''
from fastapi import APIRouter, Depends
from dependencies.jwt import get_current_user
from helper.balance import create_balance_trx, \
    get_balances, reverse_balance_trx
from models.classes import UserClass
from models.model import MerchRequestSimpleSchema, MessageGeneralSchema
from models.modelbalance import BalanceModel

# from auth.auth_handler import *

routerbalance = APIRouter(
    prefix="/balance",
    tags=["balance"],
    responses={404: {"description": "Pull Not found"}}
)


@routerbalance.get("/health")
def health():
    '''method docstring'''
    return {"pull_is_alive": True}


@routerbalance.post("/create")
async def create(
    balance: BalanceModel
):
    '''create a new balance transaction from postman'''
    res = await create_balance_trx(balance)
    return res


@routerbalance.post("/reverse", tags=["user"])
async def reverse(
    request: MessageGeneralSchema,
    current_user: UserClass = Depends(get_current_user)
):
    '''create a new balance transaction from postman'''
    res = await reverse_balance_trx(
        request,
        tokenusr=current_user)
    # return res
    return res


@routerbalance.post("/balances")
async def balances(
    request: MerchRequestSimpleSchema
):
    '''get the balances of all merchants'''
    return get_balances(request)

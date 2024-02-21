
'''Helper functions for Merchant stuff'''
from typing import List
from couchdb import Server
from dependencies.get_db import get_dbmerchant
from models.modelmerch import MerchFeeModel


def get_fees(amnt: float, m: List[MerchFeeModel]):
    '''calculates the fees for the transaction'''
    fee: float = 0
    item: MerchFeeModel
    if m is None or m == []:
        return 0
    for item in m:
        if item.ftype == "rate" and \
            item.val > 0 and \
                item.active:
            fee += (amnt * item.val / 100)
    return fee


def merchant_is_active(merchant: str = "", dbm: Server = get_dbmerchant()):
    '''calculates the fees for the transaction'''
    is_active = False
    if merchant == "":
        return False

    view_result = dbm.view(
        'Merchant/vIsActive',
        key=merchant,
        include_docs=False)

    is_active = view_result.rows[0].value if len(
        view_result.rows) > 0 else False

    return is_active


def processor_is_active(
    merchant: str = "",
    processor: str = "",
    dbm: Server = get_dbmerchant()
):
    '''calculates the fees for the transaction'''
    # http://localhost:6984/w_merchants/_design/Merchant/_view/vProcIsActive?key=["latcorp","netcashach"]
    is_active = False
    if merchant == "" or processor == "":
        return False

    view_result = dbm.view(
        'Merchant/vProcIsActive',
        key=[merchant, processor],
        include_docs=False)

    is_active = view_result.rows[0].value if len(
        view_result.rows) > 0 else False

    return is_active

'''merchant routes'''
import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from couchdb import Server
from dependencies.get_db import get_dbmerchant
from helper.counter import counter_next
from helper.merchants import merchant_is_active, processor_is_active
from models.modelmerch import MerchFeeModel, MerchModel, MerchProcessorModel

# from auth.auth_handler import *

routermerch = APIRouter(
    prefix="/merchant",
    tags=["merchant"],
    responses={404: {"description": "Pull Not found"}}
)


@routermerch.get("/health")
def health():
    '''method docstring'''
    return {"pull_is_alive": True}


@routermerch.get("/listactive", tags=["merchant"])
async def get_merchants_active(
    dbm: Server = Depends(get_dbmerchant)
) -> List[str]:
    '''get all active merchant names'''

    activemerchants: List[str] = []
    view_result = dbm.view(
        'Merchant/vListActive',
        include_docs=False)

    # Extract documents from the view result
    activemerchants = [row.value for row in view_result]

    return activemerchants


@routermerch.get("/processoractive")
async def processoractive(
    merchant: str,
    processor: str
):
    '''get the active status of a processor object'''
    is_active = False
    try:
        is_active = processor_is_active(merchant, processor)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error quering merchant: {exc}') from exc

    # return {'message': f'Successfuly
    # uploaded {[file.filename for file in files]}'}
    return is_active


@routermerch.post("/createprocessor")
async def createprocessor(
    processor: MerchProcessorModel,
    dbm: Server = Depends(get_dbmerchant)
):
    '''insert new processor definition'''
    detail = ""
    try:
        # Query the view
        # doc.merchant, doc.processor, doc.active
        detail = "processor... "
        if processor.id is not None and processor.id != "":
            myproc = dbm.get(processor.id)
            if myproc is not None and myproc["active"]:
                myproc["active"] = False
                myproc["modifieds"] = time.time()
                dbm.save(myproc)
                detail += "deactivated - "
        else:
            results = dbm.view('Merchant/vNewestFees',
                               startkey=[processor.merchant,
                                         processor.processor, True],
                               endkey=[processor.merchant,
                                       processor.processor, True])
            processor.id = \
                f'{processor.merchant}_{processor.processor}_{
                    counter_next("counter_proc")}'

            # Print the most recent document for the additional key
            if len(results.rows) > 0:
                for row in results.rows:
                    result = row.value
                    result["active"] = False
                    result["deactivated"] = time.time()
                    dbm.save(result)
                detail += "deactivated - "

            newdoc = processor.to_dict()
            newdoc["active"] = True

            dbm.save(newdoc)
            detail += "new processor added"
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error updating \
                the transaction: {exc}') from exc

    # return {'message': f'Successfuly uploaded
    # {[file.filename for file in files]}'}
    return {'message': 'ok', 'msg': detail}


@routermerch.post("/createfee")
async def createfee(
    fee: MerchFeeModel,
    dbm: Server = Depends(get_dbmerchant)
):
    '''method docstring'''
    detail = ""
    try:
        detail = "fee... "
        # Query the view
        # doc.merchant, doc.processor, doc.ftype, doc.fname, doc.active
        #
        # 1. A direct request to deactivate a fee:
        if fee.id is not None and fee.id != "":
            myfee = dbm.get(fee.id)
            if myfee is not None and myfee["active"]:
                myfee["active"] = False
                dbm.save(myfee)
                detail += "deactivated - "
        #
        # 2. A normal request to create a new fee:
        else:
            results = dbm.view('Merchant/vNewestFees',
                               startkey=[fee.merchant,
                                         fee.processor,
                                         fee.ftype,
                                         fee.fname,
                                         True],
                               endkey=[fee.merchant, fee.processor,
                                       fee.ftype, fee.fname, True])
            fee.id = \
                f'{fee.merchant}_{fee.processor}_fee_{
                    counter_next("counter_fee")}'
            newdoc = fee.to_dict()
            newdoc["active"] = True
            #
            # 2.1 Check if there are previouos definitions
            if len(results.rows) > 0:
                #
                # 2.1.1 previous definitions are deactivated
                for row in results.rows:
                    result = row.value
                    result["deactivated"] = time.time()
                    result["active"] = False
                    dbm.save(result)
                detail += "deactivated - "

            #
            # 2.2 insert the new fee:
            dbm.save(newdoc)
            detail += "new added"
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error updating \
                the transaction: {exc}') from exc

    # return {'message': f'Successfuly uploaded
    # {[file.filename for file in files]}'}
    return {'message': 'ok', 'msg': detail}


@routermerch.post("/createupdate")
async def createupdate(
    merchant: MerchModel,
    db: Server = Depends(get_dbmerchant)
):
    '''method docstring'''
    detail = ""
    try:
        doc = db.get(merchant.id)
        if doc is None:
            doc = merchant.to_dict()
            doc["_id"] = merchant.id
            doc["createds"] = time.time()
            doc["modifieds"] = doc["createds"]
        else:
            doc["_id"] = merchant.id
            doc["email"] = merchant.email
            doc["type"] = merchant.type
            doc["active"] = merchant.active
            doc["modifieds"] = time.time()

        db[merchant.id] = doc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error updating \
                the transaction: {exc}') from exc

    # return {'message': f'Successfuly uploaded
    # {[file.filename for file in files]}'}
    return {'message': 'ok', 'msg': detail}


@routermerch.get("/merchantactive")
async def merchant_active(
    merchant: str,
    dbm: Server = Depends(get_dbmerchant)
):
    '''get the active status of a merchant object'''
    try:
        is_active = merchant_is_active(merchant, dbm)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error quering merchant: {exc}') from exc

    # return {'message': f'Successfuly uploaded
    # {[file.filename for file in files]}'}
    return is_active

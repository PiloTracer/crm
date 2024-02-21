'''Methods for balance transactions'''
from datetime import datetime
import time

from couchdb import Server
from controllers.save_message import validate_request
from dependencies.get_db import get_dbbalance, get_dbmerchant, get_dbusr
from dependencies.jwt import get_current_user
from helper.merchants import get_fees
from models.classes import UserClass
from models.modelbalance import BalanceModel
from models.model import MerchRequestSimpleSchema, MessageGeneralSchema
from models.modelmerch import MerchFeeModel


def get_balances(
    request: MerchRequestSimpleSchema,
    dbb: Server = None
):
    '''Receives a balance transaction'''
    # dbb = get_dbbalance()
    # http://localhost:6984/w_balance/_design/trx/_view/balance?key="latcorp"&group=true&include_docs=false
    if dbb is None:
        dbb = get_dbbalance()

    try:

        if request.context == "":
            if request.merchant \
                    and request.merchant != "" \
                    and request.merchant != "*":
                view_result = dbb.view(
                    'trx/balance',
                    startkey=[request.merchant, "-", None],
                    endkey=[request.merchant, "-", {}],
                    group=True,
                    include_docs=False)
            else:
                view_result = dbb.view(
                    'trx/balance',
                    group=True,
                    include_docs=False)
        else:
            if request.merchant \
                    and request.merchant != "" \
                    and request.merchant != "*":
                view_result = dbb.view(
                    'trx/balance',
                    key=[request.merchant, "-", request.context],
                    group=True,
                    include_docs=False)
            else:
                view_result = dbb.view(
                    'trx/balance_context',
                    startkey=[request.context, "-", None],
                    endkey=[request.context, "-", {}],
                    group=True,
                    include_docs=False)

        # Extract documents from the view result
        queried_documents = [row for row in view_result.rows]

        if len(queried_documents) == 0:
            queried_documents = [
                {
                    "key": "n/a",
                    "value": {
                        "amntsign": 0,
                        "feesign": 0,
                        "totsign": 0
                    }
                }
            ]

    except Exception as exc:  # pylint: disable=broad-exception-caught
        # raise HTTPException(
        #    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #    detail=f'There was an error inserting
        #    the Balance Trx: {exc}') from exc
        return {
            'message': 'nok',
            'id': None,
            'rev': None,
            'error': f'There was an error querying the balances: {exc}'
        }
    return queried_documents


async def reverse_balance_trx(
    request: MessageGeneralSchema,
    tokenusr: UserClass
):
    '''Reverses a Balance Transaction'''
    #
    # Validates the user requesting the action
    dbu = get_dbusr()
    dbb = get_dbbalance()

    user = dbu.get(request.username)
    res = {
        'message': 'nok',
        'id': None,
        'rev': None,
        'error': 'Failed to proceed with validation and processing',
        'doc': None
    }
    ok = await validate_request(
        tokenusr=tokenusr,
        udoc=user)

    try:
        #
        # 1.
        # Retrieve the transaction to be reversed and mark it as reversed
        if ok:
            doc = dbb[request.message]
            doc["reversed"] = True
            # pylint: disable=unused-variable
            doc_id, doc_rev = dbb.save(doc)
            #
            # 2.
            # create reverse de transaction:
            doc.pop("_id", None)
            doc.pop("_rev", None)
            doc["created"]["id"] = request.username
            doc["created"]["merchant"] = request.merchant
            doc["created"]["created"] = time.time()
            doc["created"]["createdf"] = \
                datetime.now().strftime('%Y%m%d%H%M%S')
            doc["status"]["amntsign"] *= -1
            doc["status"]["feesign"] *= -1
            doc["status"]["totsign"] *= -1
            doc["trxtype"] = \
                "refund" if doc["type"] == "debit" \
                else "chargeback"
            doc["type"] = "credit" if doc["type"] == "debit" else "debit"
            doc["reference"] = doc_id
            #
            # 3. Save the new reversal transaction
            # pylint: disable=unused-variable
            doc_id, doc_rev = dbb.save(doc)
            view_result = dbb.view(
                'trx/by_id',
                key=doc_id,
                include_docs=False)
            doc = view_result.rows[0].value
            doc["message"] = "ok"

            res = {
                'message': 'ok',
                'id': doc_id,
                'rev': doc_rev,
                'error': None,
                'doc': doc
            }
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # raise HTTPException(
        #    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #    detail=f'There was an error inserting
        # the Balance Trx: {exc}') from exc
        res = {
            'message': 'nok',
            'id': None,
            'rev': None,
            'error': f'There was an error reversing the Balance Trx: {exc}',
            'doc': None
        }

    return res


async def create_balance_trx(
    balance: BalanceModel
):
    '''Receives a balance transaction'''
    dbm = get_dbmerchant()
    dbb = get_dbbalance()
    doc_id = ""
    # doc_rev = ""
    res = {
        'message': 'nok',
        'id': "n/a",
        'rev': "n/a",
        'error': None,
        'doc': {'message': 'nok'}
    }
    try:
        u: UserClass = await get_current_user(balance.token)
        if u.username != balance.created.id:
            raise ValueError(
                "Invalid Request Parameters - Failed to validate user")

        # Get the balance for this merchant
        req = MerchRequestSimpleSchema(
            username=balance.created.id,
            merchant=balance.merchant.merchant,
            context=balance.context
        )
        currentbal = get_balances(req, dbb)
        #
        ######################
        #
        # created
        balance.created.created = time.time()
        balance.created.createdf = datetime.now().strftime('%Y%m%d%H%M%S')
        # status:
        balance.status.status = "approved"
        balance.status.feesign = \
            (-1 * abs(balance.fee)
             ) if balance.type == 'debit' \
            else abs(balance.fee)
        balance.status.amntsign = \
            (-1 * abs(balance.amnt)
             ) if balance.type == 'debit' else \
            abs(balance.amnt)
        balance.status.tot = balance.amnt + balance.fee
        balance.status.totsign = \
            balance.status.amntsign + balance.status.feesign
        # Merchant:
        balance.merchant.bank_name = "n/a"
        balance.merchant.branch = "n/a"
        # Main:
        balance.amnt = abs(balance.amnt)
        # Re-calculate fees:
        ofees = dbm.view('Merchant/vFees',
                         key=[balance.merchant.merchant, balance.method, True])
        if len(ofees.rows) > 0:
            ofees = [MerchFeeModel(**row.value) for row in ofees]
        else:
            ofees = None
        balance.fee = get_fees(abs(balance.amnt), ofees)
        balance.exrate = 1
        #
        ######################
        #
        if currentbal[0]["value"]["totsign"] + balance.status.totsign <= 0 \
                and balance.type == 'debit':
            return {
                'message': 'nok',
                'id': None,
                'rev': None,
                'error': 'Not enough funds',
                'doc': {'message': 'nok'}
            }

        doc = balance.to_dict_noid()
        doc_id, doc_rev = dbb.save(doc)

        view_result = dbb.view(
            'trx/by_id',
            key=doc_id,
            include_docs=False)

        finaldoc = view_result.rows[0].value
        finaldoc["message"] = 'ok'

        res = {
            'message': 'ok',
            'id': doc_id,
            'rev': doc_rev,
            'error': None,
            'doc': finaldoc
        }

        # res = dbb.get(doc_id)

    except Exception as exc:  # pylint: disable=broad-exception-caught
        # raise HTTPException(
        #    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #    detail=f'There was an error inserting
        # the Balance Trx: {exc}') from exc
        res = {
            'message': 'nok',
            'id': None,
            'rev': None,
            'error': f'There was an error inserting the Balance Trx: {exc}',
            'doc': {'message': 'nok'}
        }

    return res
    # return {'message': 'ok', 'id': doc_id, 'rev': doc_rev}

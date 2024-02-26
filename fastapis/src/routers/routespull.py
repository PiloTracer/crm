'''this is a description'''
from datetime import datetime
import time
import json
import pathlib
from typing import List
import aiofiles
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from couchdb import Server
import pandas
import pika
from dependencies.get_db import \
    get_dbbalance, get_dbtrx, get_dblog, get_dbmerchant, get_dbusr
from core.settings import Settings
from helper.balance import create_balance_trx
from helper.fileutils import save_uploaded_file
from helper.merchants import get_fees
from helper.parsing import validate_parsed
from models.classes import RabbitMessage, UserApiClass
from models.model import MessageSchema, MessageSchemaRef, TrxRowEcheckId, \
    TrxUpdateSchema, TrxHeadEcheck, TrxRowEcheck, MerchRequestSchema, \
    MerchRequestSimpleSchema, UserApiEmailSchema, UserApiTrxSchema
from models.modelbalance import BalanceModel
from models.modelmerch import MerchFeeModel, MerchModel, MerchProcessorModel

# from auth.auth_handler import *

routerpull = APIRouter(
    prefix="/pull",
    tags=["pull"],
    responses={404: {"description": "Pull Not found"}}
)


@routerpull.get("/health")
def health():
    '''method docstring'''
    return {"pull_is_alive": True}


@routerpull.post("/updatetrx")
async def updatetrx(
    trx: TrxUpdateSchema,
    db: Server = Depends(get_dbtrx),
    dblog: Server = Depends(get_dblog),
    # dbm: Server = Depends(get_dbmerchant)
):
    '''method docstring'''
    settings = Settings()
    directory = settings.general_log_path
    actions: List[str] = []
    doc_id = ""  # pylint: disable=unused-variable
    doc_rev = ""  # pylint: disable=unused-variable
    doc = {"message": "nok"}
    try:
        balance: BalanceModel = BalanceModel()
        p = "".join((
            directory, "/", "test.log"
        ))
        x = json.dumps(trx.to_dict())
        async with aiofiles.open(f'{p}', 'w') as f:
            await f.write(x)

        doc_id, doc_rev = dblog.save(trx.to_dict())
        doc = db.get(trx.id)
        if doc:
            actions.append("Transaction found")
            doc["message"] = "nok"
            doc["status"] = trx.status
            doc["descriptor"] = trx.descriptor
            doc["reference"] = trx.reference
            doc["reason"] = trx.reason
            doc["createdf"] = datetime.fromtimestamp(doc["createds"]).\
                strftime('%m-%d-%Y %H:%M:%S')

            if trx.status in ["approved", "reversed"]:
                actions.append(f"Transaction {trx.status}")
                # created:
                balance.created.id = trx.username
                balance.created.merchant = trx.by_merchant
                # status:
                balance.status.status = "approved"
                balance.status.detail = f"Origen status: {trx.status}"
                # merchant:
                balance.merchant.merchant = trx.merchant
                balance.merchant.id = "n/a"
                balance.merchant.customer = trx.transaction.target
                # main:
                balance.type = trx.transaction.type
                balance.context = \
                    "withdrawal" if trx.transaction.type == "debit" \
                    and trx.transaction.trxtype == "payout" \
                    else "n/a"
                balance.trxtype = \
                    "payout" if trx.status == "approved" \
                    else "refund" if trx.status == "reversed" else "n/a"
                balance.amnt = trx.transaction.amnt
                balance.fee = trx.transaction.fees
                balance.method = trx.transaction.method
                balance.description = trx.transaction.description
                balance.reference = trx.id
                balance.currency = trx.transaction.currency
                balance.channel = trx.transaction.channel
                balance.token = trx.transaction.token
                balance.checksum = trx.transaction.checksum
                balance.origen = doc["origen"]
                # Create the balance transaction
                res = await create_balance_trx(balance)

                if res["message"] == "ok":
                    actions.append("Adjustment inserted")
                    db.save(doc)
                    doc["message"] = "ok"
                else:
                    doc = db.get(trx.id)
                    doc["message"] = "nok"
                    actions.append("Failed to create transaction")
                    raise ValueError("Failed transaction")

            db.save(doc)
            doc["message"] = "ok"

    # pylint: disable=unused-variable, broad-exception-caught
    except Exception as exc:
        doc["message"] = "nok"
        doc["error"] = exc
        # raise HTTPException(
        #    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #    detail=f'There was an error updating the
        #    transaction: {exc} - {doc_rev}') from exc
    finally:
        dblog.save(
            {
                "created_by": trx.username,
                "actions": actions,
                "doc": doc
            }
        )

    return doc


@routerpull.get("/testurl")
def test(filename: str):
    '''test method'''
    return filename
# 10.5.0.6


@routerpull.get("/testcode")
def testcode():
    '''method description'''
    dbm: Server = get_dbmerchant()
    merch = "latcorp"
    method = "netcashach"
    omerch: MerchModel = MerchModel(**dbm.get(merch))
    # doc.merchant, doc.processor
    # http://localhost:6984/w_merchants/_design/Merchant/_view/vProcessors?key=["latcorp","netcashach"]
    oprocessor = dbm.view('Merchant/vProcessors',
                          key=[merch, method], limit=1)
    if len(oprocessor.rows) > 0:
        oprocessor = MerchProcessorModel(**oprocessor.rows[0].value)
    else:
        oprocessor = None
    # doc.merchant, doc.processor, doc.active
    # http://localhost:6984/w_merchants/_design/Merchant/_view/vFees?key=["latcorp","netcashach",true]
    ofees = dbm.view('Merchant/vFees',
                     key=[merch, method, True])
    if len(ofees.rows) > 0:
        ofees = [MerchFeeModel(**row.value) for row in ofees]
    else:
        ofees = None

    return [omerch, oprocessor, ofees]


@routerpull.post("/api/auth")
async def get_api_auth(
    request: UserApiEmailSchema,
    dbu: Server = Depends(get_dbusr),
):
    '''Add a transaction through API'''
    doc = dbu.get(request.email)
    if (doc
            and doc["apitoken"]
            and doc["apisecret"]
            and doc["apitoken"] == request.apitoken):
        return {
            "message": "ok",
            "merchant": doc["merchant"],
            "apitoken": doc["apitoken"],
            "apisecret": doc["apisecret"]
        }
    else:
        return {
            "message": "nok"
        }


@routerpull.post("/transaction/add")
async def transaction_add(
    request: UserApiTrxSchema,
    dbu: Server = Depends(get_dbusr),
    dbm: Server = Depends(get_dbmerchant),
    db: Server = Depends(get_dbtrx)
):
    '''Add a transaction through API'''

    #
    # Default response message
    message: MessageSchemaRef = MessageSchemaRef(
        status='nok', message='failed', reference=None, error='default error')

    #
    # Validate the request
    oprocessor = dbm.view('Merchant/vProcessors',
                          key=[request.merchant, request.method], limit=1)
    if len(oprocessor.rows) > 0:
        oprocessor = MerchProcessorModel(**oprocessor.rows[0].value)
    else:
        oprocessor = None
    ouser: UserApiClass = UserApiClass(**dbu.get(request.authemail))
    omerch: MerchModel = MerchModel(**dbm.get(ouser.merchant))
    if (ouser.apitoken != request.apikey
        or ouser.active is False
            or omerch.active is False
            or oprocessor is None
            or oprocessor.active is False):
        message.error = "failed to validate the request"
        return message

    #
    # Get and calculate fees
    ofees = dbm.view('Merchant/vFees',
                     key=[ouser.merchant, request.method, True])
    if len(ofees.rows) > 0:
        ofees = [MerchFeeModel(**row.value) for row in ofees]
    else:
        ofees = None
    if ofees is None or len(ofees) == 0:
        message.error = "no active fees available for this method"
        return message

    #
    # Prepare the transaction
    line: TrxRowEcheckId = TrxRowEcheckId(
        customeraccount=request.customeraccount,
        amount=float(request.amount),
        cxname=request.cxname,
        routing=request.routing,
        bankaccount=request.bankaccount,
        accounttype=request.accounttype,
        email=request.email,
        address=request.address,
        trxtype=request.trxtype,
        fees=get_fees(abs(float(request.amount)), ofees),
        parent="direct",
        merchant=request.merchant,
        type="row",
        method=request.method,
        created=int(datetime.fromtimestamp(time.time()).
                    strftime('%Y%m%d%H%M%S')),
        modified=int(datetime.fromtimestamp(time.time()).
                     strftime('%Y%m%d%H%M%S')),
        createds=time.time(),
        modifieds=time.time(),
        status="pending",
        descriptor=None,
        reference=None,
        reason=None,
        comment=request.comment,
        origen=request.origen,
        id=request.id
    )

    doc = line.to_dict()

    # pylint: disable=unused-variable
    doc_id, doc_rev = db.save(doc)
    if doc_id is not None and doc_id != "":
        message.status = "ok"
        message.message = "transaction added"
        message.error = None
        message.reference = doc_id

    return message


@routerpull.get("/loadfile")
def uploads(
    filename: str,
    db: Server = Depends(get_dbtrx),
    dbm: Server = Depends(get_dbmerchant)
):
    '''method description'''
    settings = Settings()
    directory = settings.general_upload_path
    validation_results = {"status": "nok"}

    file_list = []
    inserted_document_ids = []
    week_ago = time.time() - 7 * 24 * 60 * 60

    o_file = pathlib.Path(f'{directory}/{filename}')
    message: MessageSchema = MessageSchema(status='ok', message='Success')

    if o_file.exists():
        dir_entries = [o_file]
        # with os.scandir(directory) as dir_entries:
        for entry in dir_entries:
            ext = pathlib.Path(entry.name).suffix
            excel_data_df = ""
            l1 = []
            count = 0
            total = 0
            suma = 0
            col = entry.name.split("_")
            merch = col[2].lower()
            method = col[3].lower()
            #############################
            #
            #
            omerch: MerchModel = MerchModel(**dbm.get(merch))
            if omerch is None or omerch.active is False:
                message.status = 'nok'
                message.message = "merchant is not active"
                break
            # doc.merchant, doc.processor
            # http://localhost:6984/w_merchants/_design/Merchant/_view/vProcessors?key=["latcorp","netcashach"]
            oprocessor = dbm.view('Merchant/vProcessors',
                                  key=[merch, method], limit=1)
            if len(oprocessor.rows) > 0:
                oprocessor = MerchProcessorModel(**oprocessor.rows[0].value)
            else:
                oprocessor = None
            if oprocessor is None or oprocessor.active is False:
                message.status = 'nok'
                message.message = "processor is not active"
                break
            # doc.merchant, doc.processor, doc.active
            # http://localhost:6984/w_merchants/_design/Merchant/_view/vFees?key=["latcorp","netcashach",true]
            ofees = dbm.view('Merchant/vFees',
                             key=[merch, method, True])
            if len(ofees.rows) > 0:
                ofees = [MerchFeeModel(**row.value) for row in ofees]
            else:
                ofees = None
            if ofees is None or len(ofees) == 0:
                message.status = 'nok'
                message.message = "no active fees"
                break
            #
            #
            #############################
            # if (ext == ".txt"):
            #    rows = pandas.read_csv(f"{directory}{entry.name}")
            if ext == ".xlsx":
                excel_data_df = \
                    pandas.read_excel(
                        f"{directory}/{entry.name}",
                        sheet_name='E-Check',
                        engine='openpyxl',
                        header=0,
                        converters={
                            'CX Name': str,
                            'Customer Account': str,
                            'Amount': str,
                            'Routing #': str,
                            'Bank Account #': str})\
                    .assign(parent=col[1])\
                    .rename(
                        columns=lambda x: x.strip().
                        replace(" ", "").
                        replace("#", "").lower())
                for column in excel_data_df.select_dtypes(include=[object]).columns:  # noqa: E501
                    # Remove leading and trailing spaces
                    excel_data_df[column] = excel_data_df[column].str.strip()
                    excel_data_df[column] = excel_data_df[column].str.replace(
                        r'\s+', ' ', regex=True)  # Convert multiple spaces to one # noqa: E501
                    # Convert to lower case
                    excel_data_df[column] = excel_data_df[column].str.lower()

                # Get a string with all the column
                # headers separated by pipe "|"
                column_headers: str = "|".join(excel_data_df.columns)
                validation_results = validate_parsed(
                    o_file, method, excel_data_df, column_headers)
                if validation_results.status is False:
                    message.status = 'nok'
                    message.message = "validation failed"
                    break

                tmp = excel_data_df.values.tolist()
                for t in tmp:
                    try:
                        line: TrxRowEcheck = TrxRowEcheck(*t)
                        line.amount = float(line.amount)
                    except Exception as e:  # pylint: disable=broad-except
                        detail = f'There was an error hydrating row: {e}'
                        return detail
                    if f"{line.customeraccount}" == "total":
                        total = line.amount
                        count = int(line.cxname)
                    else:
                        line.fees = get_fees(abs(line.amount), ofees)
                        line.method = method
                        line.status = "pending"
                        line.merchant = merch
                        line.created = \
                            int(datetime.fromtimestamp(entry.stat().st_ctime).
                                strftime('%Y%m%d%H%M%S'))
                        line.modified = \
                            int(datetime.fromtimestamp(entry.stat().st_mtime).
                                strftime('%Y%m%d%H%M%S'))
                        line.createds = entry.stat().st_ctime
                        line.modifieds = entry.stat().st_mtime
                        line.parent = col[1]
                        l1.append(line)
                        suma += line.amount
                        count += 1

            if entry.is_file and entry.stat().st_mtime > week_ago:
                try:
                    doc = TrxHeadEcheck()
                    doc.id = col[1]
                    doc.type = "FILE"
                    doc.method = method
                    doc.merchant = merch
                    doc.src = "fileup"
                    doc.name = str(entry.name)
                    doc.ext = ext
                    doc.path = directory
                    doc.size = entry.stat().st_size
                    doc.createds = entry.stat().st_ctime
                    doc.modifieds = entry.stat().st_mtime
                    doc.created = \
                        int(datetime.fromtimestamp(doc.createds).
                            strftime('%Y%m%d%H%M%S'))
                    doc.modified = \
                        int(datetime.fromtimestamp(doc.modifieds).
                            strftime('%Y%m%d%H%M%S'))
                    doc.content = ""
                    doc.fullpath = f"{directory}/{entry.name}"
                    doc.duplicate = False
                    doc.count = count
                    doc.total = total
                    doc.sum = suma
                    if col[1] not in db:
                        # pylint: disable=unused-variable
                        doc_id, doc_rev = db.save(doc.to_dict())
                        inserted_document_ids.append(doc_id)
                        file_list.append(doc)
                        item: TrxRowEcheck
                        for item in l1:
                            doc_id, doc_rev = db.save(item.to_dict())
                            inserted_document_ids.append(doc_id)
                except Exception as e:  # pylint: disable=broad-except
                    detail = f'There was an error inserting the header: {e}'
                    return detail

                # transactions += rows
    return inserted_document_ids


@routerpull.post("/filesupload")
async def filesupload(files: List[UploadFile]):
    """Upload multiple files."""
    settings = Settings()
    directory = settings.general_upload_path
    prefix = datetime.now().strftime('%Y%m%d')
    try:
        uploaded_files = []
        for file in files:
            filename, st = \
                await save_uploaded_file(file, directory, prefix)
            if st is not False:
                uploaded_files.append(filename)
                await publishnewfile(filename)
        return {'message': 'ok', 'uploaded_files': uploaded_files}
    # pylint: disable=unused-variable, broad-exception-caught
    except Exception as exc:  # noqa: F841
        return {'message': 'nok',
                'msg': "There was an error uploading the file(s)"}


async def publishnewfile(filename):
    '''publishing a message to rabbitmq'''

    ele = filename.split("_")
    vdate = ele[0]  # pylint: disable=unused-variable # noqa: F841
    vchecksum = ele[1]  # pylint: disable=unused-variable # noqa: F841
    merch = ele[2]  # pylint: disable=unused-variable # noqa: F841
    message: RabbitMessage = RabbitMessage()
    message.type = "upload"
    message.channel = "newfile"
    message.header = "newfile"
    message.message = filename
    message.merchant = merch

    credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('srv.rabbitmq', 5672, '/', credentials))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='newfile')

    # Publish a message
    jsonstring = json.dumps(message.__dict__)
    channel.basic_publish(
        exchange='', routing_key='newfile', body=jsonstring)

    connection.close()


@routerpull.post("/transactions")
def transactions(
    mrequest: MerchRequestSchema,
    db: Server = Depends(get_dbtrx),
    dbu: Server = Depends(get_dbusr)
):
    '''some description'''
    output = []

    try:
        # http://localhost:6984/w_trx/_design/trx/_view/by_fields?startkey=[%22row%22,%22netcashach%22]&endkey=[%22row%22,%22netcashach%22,{}]
        # http://localhost:6984/w_trx/_design/trx/_view/by_fields?startkey=[%22row%22,%22netcashach%22,%22latcorp%22]&endkey=[%22row%22,%22netcashach%22,%22latcorp%22]
        user = dbu.get(mrequest.username)
        if "owner" == user["role"]:
            skey = ['row', mrequest.method]
            ekey = ['row', mrequest.method, {}]
        else:
            skey = ['row', mrequest.method, mrequest.merchant]
            ekey = ['row', mrequest.method, mrequest.merchant]

        # Query the view to get documents with the specified values
        view_result = db.view(
            'trx/by_fields',
            startkey=skey,
            endkey=ekey,
            include_docs=True)

        # Extract documents from the view result
        queried_documents = [row['doc'] for row in view_result.rows]

        # Print the queried documents
        for document in queried_documents:
            # datetime.fromtimestamp(entry.stat().st_mtime).strftime('%Y%m%d%H%M%S')

            output.append({
                "_id": document["_id"],
                "createds": document["createds"],
                "createdf": datetime.fromtimestamp(document["createds"]).
                strftime('%m-%d-%Y %H:%M:%S'),
                "customeraccount": document["customeraccount"],
                "amount": document["amount"],
                "merchant": document["merchant"],
                "cxname": document["cxname"],
                "routing": document["routing"],
                "bankaccount": document["bankaccount"],
                "accounttype": document["accounttype"],
                "email": document["email"],
                "address": document["address"],
                "trxtype": document["trxtype"],
                "fees": document["fees"],
                "parent": document.get('parent', ''),
                "type": document["type"],
                "method": document["method"],
                "status": document.get('status', ''),
                "reason": document.get('reason', ''),
                "reference": document.get('reference', ''),
                "descriptor": document.get('descriptor', '')
            })

    except db.ServerError as e:
        print(f"Error connecting to CouchDB: {e}")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error connecting to the db') from exc

    return output


@routerpull.post("/adjustments")
def adjustments(
    mrequest: MerchRequestSimpleSchema,
    db: Server = Depends(get_dbbalance)
):
    '''some description'''
    # value1_to_query = mrequest.merchant

    try:
        # Query the view to get documents with the specified values
        # http://admin:admin123@localhost:6984/w_balance/_design/trx/_view/by_merchant?key=["LATCORP"]
        if mrequest.merchant == "*":
            view_result = db.view(
                'trx/by_merchant',
                include_docs=False)
        else:
            view_result = db.view(
                'trx/by_merchant',
                key=[mrequest.merchant],
                include_docs=False)

        queried_documents = [row.value for row in view_result]

    except db.ServerError as e:
        print(f"Error connecting to CouchDB: {e}")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='There was an error connecting to the db') from exc

    return queried_documents

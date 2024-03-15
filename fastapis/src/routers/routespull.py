'''this is a description'''
from datetime import datetime
import time
import json
import pathlib
from typing import List
import traceback
import aiofiles
from fastapi import APIRouter, Body, Depends, UploadFile, HTTPException, status
from couchdb import Server
import pandas
from pydantic import ValidationError

from dependencies.get_db import \
    get_dbbalance, get_dblogtrx, get_dbtrx, \
    get_dblog, get_dbmerchant, get_dbusr
from core.settings import Settings
from helper.balance import create_balance_trx
from helper.counter import counter_next
from helper.fileutils import save_uploaded_file
from helper.logging import log_and_return_message, publishnewfile
from helper.merchants import get_fees
from helper.parsing import validate_file_struct
from helper.bloomfilter import is_duplicate_transaction
from models.classes import UserApiClass
from models.model import (
    MessageSchema,
    MessageSchemaRef,
    TrxRowEcheckId,
    TrxRowEcheckSignature,
    TrxUpdateSchema,
    TrxHeadEcheck,
    TrxRowEcheck,
    MerchRequestSchema,
    MerchRequestSimpleSchema,
    UserApiEmailSchema)
from models.modelbalance import BalanceModel
from models.modelhelper import LogTrxModel
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
    request: dict = Body(...),
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
        trx = TrxUpdateSchema.model_validate(request)
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
            doc["modifieds"] = time.time()
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
                balance.origen = doc.get("origen", "unknown")
                # Create the balance transaction
                res = await create_balance_trx(balance)

                if res["message"] == "ok":
                    actions.append("Adjustment inserted")
                    db.save(doc)
                    doc["message"] = "ok"
                else:
                    doc = db.get(trx.id)
                    actions.append("Failed to create transaction")
                    raise ValueError("Failed transaction")

            db.save(doc)
            doc["message"] = "ok"

    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            # pylint: disable = unused-variable
            field = error["loc"][-1]  # noqa: F841
            msg = error["msg"]
            error_messages.append(f"Error: {msg}({field})")
        doc["error"] = ", ".join(error_messages)
    # pylint: disable=unused-variable, broad-exception-caught
    except Exception as exc:
        doc["message"] = "nok"
        doc["error"] = str(exc)
        # raise HTTPException(
        #    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #    detail=f'There was an error updating the
        #    transaction: {exc} - {doc_rev}') from exc
    finally:
        dblog.save(
            {
                "created_by": request["username"],
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


@routerpull.post("/transaction/create")
async def transaction_create(
    request: dict = Body(...)
):
    '''Add a manual transaction'''
    result = {
        'status': "failed",
        'message': "nok",
        'reference': "n/a",
        'error': "some error"
    }
    try:
        request["origen"] = "main"
        request["_id"] = f"{request["merchant"]}_{request["method"]}_{counter_next("manualtrx")}_u"
        result = await transaction_add(request)
    except ValidationError as e:  # pylint: disable= broad-exception-caught
        error_messages = ["Error"]
        for error in e.errors():
            # pylint: disable = unused-variable
            field = error["loc"][-1]  # noqa: F841
            msg = error["msg"]
            error_messages.append(f"Error: {msg}({field})")
        result["error"] = ", ".join(error_messages)

    except Exception as e:  # pylint: disable= broad-exception-caught
        result["error"] = str(e)

    return result  # pylint: disable = return-in-finally, lost-exception


@routerpull.post("/transaction/add")
async def transaction_add(
    request: dict = Body(...)
):
    '''Add a transaction through API'''

    dbu = get_dbusr()
    dbm = get_dbmerchant()
    db = get_dbtrx()

    message: MessageSchemaRef = MessageSchemaRef(
        status='failed',
        message='nok',
        reference=None,
        error='default error')

    try:
        # check for duplicates
        if request["origen"] == "customer" and \
            is_duplicate_transaction(request["_id"], db):
            raise ValueError("Error duplicate found")

        # validate and mutate the request
        line = TrxRowEcheckId.model_validate(
            request,
            strict=None,
            from_attributes=None)

        #
        # Default response message
        line.origen = "customer" if line.origen != "main" else "main"
        line.authemail = \
            line.authemail if line.origen != "main" \
            else line.created_by

        #
        # Validate the request
        # http://localhost:6984/w_merchants/_design/Merchant/_view/vProcessors?key=[%22cliente%22,%22netcashach%22]
        oprocessor = dbm.view('Merchant/vProcessors',
                              key=[line.merchant, line.method], limit=1)
        if len(oprocessor.rows) > 0:
            oprocessor = MerchProcessorModel(**oprocessor.rows[0].value)
        else:
            oprocessor = None
        ouser: UserApiClass = UserApiClass(**dbu.get(line.authemail))
        merch: str = ouser.merchant \
            if line.origen == "customer" \
            else line.merchant
        omerch: MerchModel = MerchModel(
            **dbm.get(merch)
        )
        if (line.origen != "main"
            and (ouser.apitoken != line.apikey
                 or ouser.active is False
                 or omerch.active is False
                 or oprocessor is None
                 or oprocessor.active is False)):
            message.error = "Error validating the request"
            return message

        #
        # Get and calculate fees
        ofees = dbm.view('Merchant/vFees',
                         key=[merch, line.method, True])
        if len(ofees.rows) > 0:
            ofees = [MerchFeeModel(**row.value) for row in ofees]
        else:
            ofees = None
        if ofees is None or len(ofees) == 0:
            message.error = "Error applying fees"
            return message

        # Set additional values
        line.fees = get_fees(abs(float(line.amount)), ofees)
        line.parent = "direct"
        line.type = "row"
        line.status = "pending"
        ####

        doc = line.to_dict(True)

        # pylint: disable=unused-variable
        doc_id, doc_rev = db.save(doc)
        message = db.get(doc_id)
        if doc_id is not None and doc_id != "":
            message["message"] = "ok"

    except ValidationError as e:  # pylint: disable= broad-exception-caught
        error_messages = ["Error"]
        for error in e.errors():
            # pylint: disable = unused-variable
            field = error["loc"][-1]  # noqa: F841
            msg = error["msg"]
            error_messages.append(f"Error: {msg}({field})")
        message.error = ", ".join(error_messages)

    except Exception as e:  # pylint: disable= broad-exception-caught
        message.error = str(e)

    return message


@routerpull.get("/loadfile")
async def uploads(
    filename: str,
    db: Server = Depends(get_dbtrx),
    dbm: Server = Depends(get_dbmerchant)
):
    '''method description'''
    settings = Settings()
    directory = settings.general_upload_path
    # validation_results = {"status": "nok"}
    merch = ""  # let's make merch variable global

    file_list = []
    inserted_document_ids = []
    week_ago = time.time() - 7 * 24 * 60 * 60

    entry = pathlib.Path(f'{directory}/{filename}')
    parts = filename.split("_")
    message: MessageSchema = MessageSchema(status='ok', message='Success')

    ##########
    # Prepare the log for this file
    db_logtrx = get_dblogtrx()
    view_result = db_logtrx.view(
        'logtrx/by_doc_id',
        key=parts[1],
        include_docs=True,
        descending=True)
    docv = view_result.rows[0].doc
    docv["extra"] = ["Processing file..."] + docv["extra"]
    ##########

    if entry.exists() is False:
        r = await log_and_return_message(
            db_logtrx,
            message,
            docv,
            "nok",
            "Error with file")
        return r

    ext = pathlib.Path(entry.name).suffix
    excel_data_df = ""
    l1 = []
    count = 0
    suma = 0
    col = entry.name.split("_")
    merch = col[2].lower()
    method = col[3].lower()
    if col[1] in db:
        r = await log_and_return_message(
            db_logtrx,
            message,
            docv,
            "nok",
            "Error file is duplicate")
        return r
    #############################
    #
    #
    m = dbm.get(merch)
    omerch: MerchModel = MerchModel(**m)
    if omerch is None or omerch.active is False:
        r = await log_and_return_message(
            db_logtrx,
            message,
            docv,
            "nok",
            "Error in merchant")
        return r
    # doc.merchant, doc.processor
    # http://localhost:6984/w_merchants/_design/Merchant/_view/vProcessors?key=["latcorp","netcashach"]
    oprocessor = dbm.view('Merchant/vProcessors',
                          key=[merch, method], limit=1)
    if len(oprocessor.rows) > 0:
        oprocessor = MerchProcessorModel(**oprocessor.rows[0].value)
    else:
        oprocessor = None
    if oprocessor is None or oprocessor.active is False:
        r = await log_and_return_message(
            db_logtrx,
            message,
            docv,
            "nok",
            "Error with processor/method")
        return r

    # doc.merchant, doc.processor, doc.active
    # http://localhost:6984/w_merchants/_design/Merchant/_view/vFees?key=["latcorp","netcashach",true]
    ofees = dbm.view('Merchant/vFees',
                     key=[merch, method, True])
    if len(ofees.rows) > 0:
        ofees = [MerchFeeModel(**row.value) for row in ofees]
    else:
        ofees = None
    if ofees is None or len(ofees) == 0:
        r = await log_and_return_message(
            db_logtrx,
            message,
            docv,
            "nok",
            "Error in fees")
        return r
    #
    #
    #############################
    # if (ext == ".txt"):
    #    rows = pandas.read_csv(f"{directory}{entry.name}")
    if ext == ".xlsx" \
            and entry.is_file \
            and entry.stat().st_mtime > week_ago:
        excel_data_df = \
            pandas.read_excel(
                f"{directory}/{entry.name}",
                sheet_name='E-Check',
                engine='openpyxl',
                header=0,
                converters={
                    'Id': str,
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
        # for column in excel_data_df.select_dtypes(include=[object]).columns:  # noqa: E501
        #    # Remove leading and trailing spaces
        #    excel_data_df[column] = excel_data_df[column].str.strip()
        #    excel_data_df[column] = excel_data_df[column].str.replace(
        #        r'\s+', ' ', regex=True)  # Convert multiple spaces to one # noqa: E501
        #    # Convert to lower case
        #    excel_data_df[column] = excel_data_df[column].str.lower()

        ##################

        # Get a string with all the column
        # headers separated by pipe "|"
        column_headers: str = "|".join(excel_data_df.columns)
        valid_structure = validate_file_struct(
            entry, method, excel_data_df, column_headers)
        if not valid_structure:
            r = await log_and_return_message(
                db_logtrx,
                message,
                docv,
                "nok",
                "Error in file structure")
            return r
        ##################
        # if validation_results.status is False:
        #    validation_results.message = "Failed Validation"
        #    message.status = 'nok'
        #    message.message = "validation failed"
        #    doc["extra"] = validation_results.__dict__
        # db_logtrx.save(doc)
        # publishnewfile(filename)
        # xxxxxxx the following code is ugly, need to fix
        # if validation_results.status is False:
        #    break

        tmp = excel_data_df.values.tolist()
        for t in tmp:
            try:
                if t[0].lower() == "total":
                    line = TrxRowEcheckSignature(
                            label=t[0],
                            total=float(t[1]),
                            count=t[2]
                    )
                else:
                    line = TrxRowEcheck(
                        customeraccount=t[1],
                        amount=float(t[2]),
                        currency="usd",
                        cxname=t[3],
                        routing=t[4],
                        bankaccount=t[5],
                        accounttype=t[6],
                        email=t[7],
                        address=t[8],
                        trxtype=t[9],
                        parent=t[10],
                        merchant=merch,
                        method=method,
                        status="pending",
                        type="row",
                        origen="file"
                    )
                    
                if isinstance(line, TrxRowEcheckSignature) and (
                        line.total != suma
                        or line.count != count):
                    raise ValueError("Total or count does not match")

                if isinstance(line, TrxRowEcheck):
                    line.id = f"{merch}_{method}_{t[0]}"
                    line.fees = get_fees(abs(line.amount), ofees)
                    #line.parent = col[1]
                    #line = TrxRowEcheck.model_validate(line)
                    l1.append(line)
                    suma += line.amount
                    count += 1

                    if is_duplicate_transaction(line.id, db):
                        raise ValueError(f"Duplicate trx in batch (row# {count})")

            except ValidationError as e:
                error_messages = []
                for error in e.errors():
                    # pylint: disable = unused-variable
                    field = error["loc"][-1]  # noqa: F841
                    msg = error["msg"]
                    error_messages.append(f"Error: {msg}({field})")
                detail = ", ".join(error_messages)

                r = await log_and_return_message(
                    db_logtrx,
                    message,
                    docv,
                    "nok",
                    detail)
                return r

            except Exception as e:  # pylint: disable=broad-except
                r = await log_and_return_message(
                    db_logtrx,
                    message,
                    docv,
                    "nok",
                    f'Error hydrating row: {str(e)}')
                return r

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
            doc.sum = suma
            if col[1] not in db:
                # pylint: disable=unused-variable
                doc_id, doc_rev = db.save(doc.to_dict())
                inserted_document_ids.append(doc_id)
                file_list.append(doc)
                item: TrxRowEcheck
                # Check for duplicates
                i = 1
                for item in l1:
                    if is_duplicate_transaction(item.id, db):
                        raise ValueError(f"Duplicate trx in row # {i}")
                    i += 1
                # Save all documents
                for item in l1:
                    trx = item.to_dict(True)
                    doc_id, doc_rev = db.save(trx)
                    inserted_document_ids.append(doc_id)
        except Exception as e:  # pylint: disable=broad-except
            r = await log_and_return_message(
                db_logtrx,
                message,
                docv,
                "nok",
                f'Error inserting the header: {
                    str(e)}')
            return r

    r = await log_and_return_message(
        db_logtrx,
        message,
        docv,
        "ok",
        f'Success! {len(l1)} trxs added')
    return r


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
        exc_type = type(exc).__name__
        exc_traceback = traceback.format_exc()

        return {'message': 'nok',
                'msg': f"Error uploading the file(s): \
                Type:: {exc_type} :: Exception:: {exc} :: \
                Traceback:: {exc_traceback} :: \
                file:: {file.filename} :: \
                directory:: {directory} :: \
                prefix:: {prefix}"}  # noqa: E501


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
                "currency": document.get('currency', 'usd'),
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


@routerpull.post("/latestuploads", response_model=List[LogTrxModel])
def get_latest_uploads(
    mrequest: MerchRequestSimpleSchema,
    dblogtrx: Server = Depends(get_dblogtrx)
) -> List[LogTrxModel]:
    '''Get the latest file parse results'''

    results = None
    # http://localhost:6984/w_log_trx/_design/logtrx/_view/lastuploads?startkey=["cliente",{}]&endkey=["cliente"]&include_docs=true&descending=true
    results = dblogtrx.view('logtrx/lastuploads',
                            startkey=[mrequest.merchant, {}],
                            endkey=[mrequest.merchant],
                            descending=True,
                            include_docs=True) \
        if mrequest.merchant != "*" \
        else dblogtrx.view('logtrx/lastuploads',
                           descending=True,
                           include_docs=True)

    documents = [row.doc for row in results.rows]

    return documents

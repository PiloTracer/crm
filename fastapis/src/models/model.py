"""class description"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MessageGeneralSchema(BaseModel):
    """standard simple message"""
    username: str
    merchant: str
    message: Optional[str] = None


class MessageResponseSchema(BaseModel):
    """standard simple response message"""
    message: Optional[str] = None
    error: Optional[str] = None


class MessageSchema(BaseModel):
    """standard simple message"""
    status: str
    message: str


class MessageSchemaRef(MessageSchema):
    """standard simple message with reference"""
    reference: Optional[str] = None
    error: Optional[str] = None


class UserLoginSchema(BaseModel):
    """docstring"""
    username: str
    password: str


class UserApiEmailSchema(BaseModel):
    """Basic Schema to receive an email element"""
    email: str
    apitoken: str


class UserApiTrxSchema(BaseModel):
    """Basic Schema to receive a new Transaction via API"""
    id: Optional[str] = Field(None, alias='_id')
    authchecksum: Optional[str] = None
    authemail: Optional[str] = None
    customeraccount: str
    amount: str
    currency: str
    fees: Optional[float] = 0
    cxname: str
    routing: str
    bankaccount: str
    accounttype: str
    email: str
    address: str
    trxtype: Optional[str] = None
    parent: Optional[str] = None
    type: Optional[str] = None
    merchant: str
    comment: Optional[str] = None
    method: str
    version: Optional[str] = "0"
    apikey: Optional[str] = None
    origen: Optional[str] = None
    created_by: Optional[str] = None
    created_merchant: Optional[str] = None

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            'id': self.id,
            'authchecksum': self.authchecksum,
            'authemail': self.authemail,
            'customeraccount': self.customeraccount,
            'amount': self.amount,
            'currency': self.currency,
            'fees': self.fees,
            'cxname': self.cxname,
            'routing': self.routing,
            'bankaccount': self.bankaccount,
            'accounttype': self.accounttype,
            'email': self.email,
            'address': self.address,
            'trxtype': self.trxtype,
            'parent': self.parent,
            'type': self.type,
            'merchant': self.merchant,
            'comment': self.comment,
            'method': self.method,
            'version': self.version,
            'apikey': self.apikey,
            'origen': self.origen,
            'created_by': self.created_by,
            'created_merchant': self.created_merchant
        }


class UserApiCreate(BaseModel):
    """Create API credentials"""
    id: str
    merchant: str
    token: Optional[str] = None
    apitoken: Optional[str] = None
    apisecret: Optional[str] = None


class MerchRequestSimpleSchema(BaseModel):
    """requests for username and a merchant"""
    username: str
    merchant: str
    context: Optional[str] = ""


class MerchRequestSchema(BaseModel):
    """requests that are related to a username and a merchant"""
    username: str
    method: str
    merchant: str


class TrxUpdateExtraBaseSchema(BaseModel):
    """Extra Data for Balance Transaction"""
    type: Optional[str] = None
    context: Optional[str] = None
    trxtype: Optional[str] = None
    amnt: float = 0
    fees: float = 0
    description: Optional[str] = None
    target: Optional[str] = None
    origen: Optional[str] = None
    currency: Optional[str] = None
    method: Optional[str] = None
    channel: Optional[str] = None
    token: Optional[str] = None
    checksum: Optional[str] = None


class TrxUpdateBaseSchema(BaseModel):
    """docstring"""
    id: Optional[str] = None
    status:     str
    descriptor: Optional[str] = None
    reference:  Optional[str] = None
    reason:     Optional[str] = None


class TrxUpdateSchema(TrxUpdateBaseSchema):
    """docstring"""
    username: Optional[str] = None
    merchant: Optional[str] = None
    by_merchant: Optional[str] = None
    created: int = int(datetime.now().strftime('%Y%m%d%H%M%S'))
    completed: bool = False
    transaction: Optional[TrxUpdateExtraBaseSchema] = None

    def to_dict(self):
        """convert TrxUpdateSchema to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            'id': self.id,
            'username': self.username,
            'merchant': self.merchant,
            'by_merchant': self.by_merchant,
            'created': self.created,
            'completed': self.completed,
            'status': self.status,
            'descriptor': self.descriptor,
            'reference': self.reference,
            'reason': self.reason,
            'transaction': {
                'type': self.transaction.type,
                'context': self.transaction.context,
                'trxtype': self.transaction.trxtype,
                'amnt': self.transaction.amnt,
                'fees': self.transaction.fees,
                'description': self.transaction.description,
                'target': self.transaction.target,
                'origen': self.transaction.origen,
                'currency': self.transaction.currency,
                'method': self.transaction.method,
                'channel': self.transaction.channel
            }
        }


class MessageUser(BaseModel):
    """docstring"""
    id: str = ""
    access_token: str = None


class TrxHeadEcheck(BaseModel):
    """docstring"""
    id: Optional[str] = ""
    type: Optional[str] = ""
    method: Optional[str] = ""
    merchant: Optional[str] = ""
    src: Optional[str] = ""
    name: Optional[str] = ""
    ext: Optional[str] = ""
    path: Optional[str] = ""
    content: Optional[str] = ""
    fullpath: Optional[str] = ""
    other: Optional[str] = ""
    size: Optional[int] = 0
    count: Optional[int] = 0
    duplicate: Optional[bool] = False
    total: Optional[float] = 0
    sum: Optional[float] = 0
    createds: Optional[float] = 0
    modifieds: Optional[float] = 0
    created: Optional[int] = 0
    modified: Optional[int] = 0

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            '_id': self.id,
            'type': self.type,
            'method': self.method,
            'merchant': self.merchant,
            'src': self.src,
            'name': self.name,
            'ext': self.ext,
            'path': self.path,
            'content': self.content,
            'fullpath': self.fullpath,
            'other': self.other,
            'size': self.size,
            'count': self.count,
            'duplicate': self.duplicate,
            'total': self.total,
            'sum': self.sum,
            'created': self.created,
            'modified': self.modified,
            'createds': self.created,
            'modifieds': self.modified
        }


class TrxHeadEcheckList:
    """docstring"""
    list: List[TrxHeadEcheck]


class PullTrxEcheck:
    """Core Transaction Data"""
    customeraccount: str = None
    amount: float = None
    currency: str = None
    cxname: str = None
    routing: str = None
    bankaccount: str = None
    accounttype: str = None
    email: str = None
    address: str = None
    trxtype: str = None
    fees: float = 0
    origen: str = None


class TrxRowEcheck(PullTrxEcheck):
    """docstring"""

    def __init__(
        self,
        customeraccount,
        amount,
        currency,
        cxname,
        routing,
        bankaccount,
        accounttype,
        email,
        address,
        trxtype=None,
        fees=0,
        parent=None,
        type="row",  # pylint: disable=redefined-builtin
        method=None,
        created=0,
        modified=0,
        createds=0,
        modifieds=0,
        merchant=None,
        status="pending",
        descriptor=None,
        reference=None,
        reason=None,
        comment=None,
        origen=None
    ):
        self.customeraccount: str = customeraccount
        self.amount: float = amount
        self.currency: str = currency
        self.cxname: str = cxname
        self.routing: str = routing
        self.bankaccount: str = bankaccount
        self.accounttype: str = accounttype
        self.email: str = email
        self.address: str = address
        self.trxtype: str = trxtype
        self.fees: float = fees
        self.parent: str = parent
        self.merchant: str = merchant
        self.type: str = type
        self.method: str = method
        self.created: int = created
        self.modified: int = modified
        self.createds: float = createds
        self.modifieds: float = modifieds
        self.merchant: str = merchant
        self.status: str = status
        self.descriptor: str = descriptor
        self.reference: str = reference
        self.reason: str = reason
        self.comment: str = comment
        self.origen: str = origen

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            'customeraccount': self.customeraccount,
            'amount': self.amount,
            'currency': self.currency,
            'cxname': self.cxname,
            'routing': self.routing,
            'bankaccount': self.bankaccount,
            'accounttype': self.accounttype,
            'email': self.email,
            'address': self.address,
            'trxtype': self.trxtype,
            'fees': self.fees,
            'parent': "" if self.parent is None else self.parent,
            'type': self.type,
            'method': self.method,
            'created': self.created,
            'modified': self.modified,
            'createds': self.createds,
            'modifieds': self.modifieds,
            'merchant': "" if self.merchant is None else self.merchant,
            'status': "pending" if self.status is None else self.status,
            'descriptor': "" if self.descriptor is None else self.descriptor,
            'reference': "" if self.reference is None else self.reference,
            'reason': "" if self.reason is None else self.reason,
            'comment': "" if self.comment is None else self.comment,
            'origen': "" if self.origen is None else self.origen
        }

    class Config:
        """docstring"""
        validate_assignment = True


class TrxRowEcheckId(TrxRowEcheck):
    """docstring"""

    def __init__(
        self,
        customeraccount,
        amount,
        currency,
        cxname,
        routing,
        bankaccount,
        accounttype,
        email,
        address,
        trxtype=None,
        fees=0,
        parent=None,
        type=None,  # pylint: disable=redefined-builtin
        method=None,
        created=0,
        modified=0,
        createds=0,
        modifieds=0,
        merchant=None,
        status="pending",
        descriptor=None,
        reference=None,
        reason=None,
        comment=None,
        origen=None,
        id=None  # pylint: disable=redefined-builtin
    ):
        super().__init__(
            customeraccount,
            amount,
            currency,
            cxname,
            routing,
            bankaccount,
            accounttype,
            email,
            address,
            trxtype,
            fees,
            parent,
            type,
            method,
            created,
            modified,
            createds,
            modifieds,
            merchant,
            status,
            descriptor,
            reference,
            reason,
            comment,
            origen
        )
        self.id: str = id

    def to_dict(self, withid: bool = True):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        d = {
            'customeraccount': self.customeraccount,
            'amount': self.amount,
            'currency': self.currency,
            'cxname': self.cxname,
            'routing': self.routing,
            'bankaccount': self.bankaccount,
            'accounttype': self.accounttype,
            'email': self.email,
            'address': self.address,
            'trxtype': self.trxtype,
            'fees': self.fees,
            'parent': "" if self.parent is None else self.parent,
            'type': self.type,
            'method': self.method,
            'created': self.created,
            'modified': self.modified,
            'createds': self.createds,
            'modifieds': self.modifieds,
            'merchant': "" if self.merchant is None else self.merchant,
            'status': "pending" if self.status is None else self.status,
            'descriptor': "" if self.descriptor is None else self.descriptor,
            'reference': "" if self.reference is None else self.reference,
            'reason': "" if self.reason is None else self.reason,
            'comment': "" if self.comment is None else self.comment,
            'origen': "" if self.origen is None else self.origen
        }
        if withid:
            d["_id"] = self.id
        return d

    class Config:
        """docstring"""
        validate_assignment = True


class TrxRowEcheckList:
    """docstring"""
    list: List[TrxRowEcheck]

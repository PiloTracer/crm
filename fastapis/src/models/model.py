"""class description"""
from datetime import datetime
import time
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from pydantic.types import constr

from helper.validor import (
    amount_validator,
    bankaccount_validator,
    digits_validator,
    email_validator,
    lowercase_validator,
    name_validator,
    regular_alphanumeric_validator,
    trxtype_validator,
    unsafe_validator
)


class BaseNetcashachSchema(BaseModel):
    '''Basic Fields for Netcashach method'''
    # pylint: disable = line-too-long
    customeraccount: Annotated[constr(strip_whitespace=True, min_length=3, max_length=20), str] = Field(..., description="Receiver's user account")  # type: ignore # noqa: E501
    amount: float = Field(..., description="Transaction amount", ge=20.0, le=1000000000.0)  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    currency: Annotated[constr(strip_whitespace=True, min_length=3, max_length=3), str] = Field(..., description="Transaction currency")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    cxname: Annotated[constr(strip_whitespace=True, min_length=5, max_length=100), str] = Field(..., description="Receiver's name")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    routing: Annotated[constr(strip_whitespace=True, min_length=5, max_length=20), str] = Field(..., description="Receiver's routing number")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    bankaccount: Annotated[constr(strip_whitespace=True, min_length=5, max_length=100), str] = Field(..., description="Receiver's bank account")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    accounttype: Annotated[constr(strip_whitespace=True, min_length=1, max_length=1), str] = Field(..., description="Receiver's account type")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    email: Annotated[constr(strip_whitespace=True, min_length=10, max_length=200), str] = Field(..., description="Receiver's email")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    address: Annotated[constr(strip_whitespace=True, min_length=10, max_length=200), str] = Field(..., description="Receiver's address")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    trxtype: Annotated[constr(strip_whitespace=True, min_length=3, max_length=20), str] = Field(..., description="Type of transaction")  # type: ignore # noqa: E501
    descriptor: Optional[str] = None
    reference: Optional[str] = None
    reason: Optional[str] = None

    _address_val_unsafe = unsafe_validator('address')
    _address_val_lowercase = lowercase_validator('address')
    _trxtype_val_trxtype = trxtype_validator('trxtype')
    _trxtype_val_lowercase = lowercase_validator('trxtype')
    _email_val_email = email_validator('email')
    _email_val_lowercase = lowercase_validator('email')
    _accounttype_val_lowercase = lowercase_validator('accounttype')
    _bankaccount_val_bankaccount = bankaccount_validator('bankaccount')
    _bankaccount_val_lowercase = lowercase_validator('bankaccount')
    _routing_val_digits = digits_validator('routing')
    _cxname_val_name = name_validator('cxname')
    _cxname_val_lowercase = lowercase_validator('cxname')
    _amount_val_amount = amount_validator('amount')
    _customeraccount_val_custaccount = regular_alphanumeric_validator('customeraccount')  # noqa: E501
    _customeraccount_val_lowercase = lowercase_validator('customeraccount')

    class Config:
        '''UserApiTrxSchema config'''
        validate_assignment = True
        validate_all = False

    def to_dict(self):
        """convert to dict"""
        return self.model_dump(by_alias=True, exclude_none=True)


class UserApiTrxSchema(BaseNetcashachSchema):
    "Basic Schema to receive a new Transaction via API"""
    # pylint: disable = line-too-long
    id: str = Field(None, alias="_id")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    fees: float = Field(default=0, description="Transaction fee", ge=0.0, le=1000000000.0)  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    authchecksum: Annotated[constr(strip_whitespace=True, min_length=3, max_length=100), Optional[str]] = Field(default=None, description="Transaction checksum")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    authemail: Annotated[constr(strip_whitespace=True, min_length=3, max_length=100), Optional[str]] = Field(default=None, description="Credentials email")  # type: ignore # noqa: E501
    parent: Optional[str] = None
    type: Optional[str] = None
    merchant: Annotated[constr(strip_whitespace=True, min_length=3, max_length=50), str] = Field(..., description="Merchant")  # type: ignore # noqa: E501
    comment: Annotated[constr(strip_whitespace=True, min_length=0, max_length=2000), str] = Field(default="", description="Merchant")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    method: Annotated[constr(strip_whitespace=True, min_length=3, max_length=50), str] = Field(..., description="Transfer method")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    version: Annotated[constr(strip_whitespace=True, min_length=3, max_length=20), Optional[str]] = Field(default="1.0", description="API version")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    apikey: Optional[str] = Field(default=None, strip_whitespace=True, description="Api Key from API credentials")  # type: ignore # noqa: E501
    origen: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    created_merchant: Optional[str] = None
    message: Optional[str] = None
    # pylint: disable = line-too-long
    created: int = Field(default_factory=lambda: int(datetime.now().strftime('%Y%m%d%H%M%S')))  # type: ignore # noqa: E501
    modified: int = created  # type: ignore # noqa: E501
    createds: float = Field(default_factory=time.time)
    modifieds: float = createds

    _id_val_alphanum = regular_alphanumeric_validator('id')
    _authchecksum_val_unsafe = unsafe_validator('authchecksum')
    _authemail_val_email = email_validator('authemail')
    _authemail_val_lowercase = lowercase_validator('authemail')
    _merchant_val_email = regular_alphanumeric_validator('merchant')
    _merchant_val_lowercase = lowercase_validator('merchant')
    _method_val_alphanum = regular_alphanumeric_validator('method')
    _method_val_lowercase = lowercase_validator('method')
    _version_val_alphanum = regular_alphanumeric_validator('version')
    _apikey_val_alphanum = regular_alphanumeric_validator('apikey')

    @classmethod
    def construct_without_validation(cls, **kwargs):
        return cls.model_construct(**kwargs)

    def to_dict(self, withid: bool = True):
        """convert to dict"""
        d = self.model_dump(exclude_none=True, by_alias=True)
        if not withid and "_id" in d:
            del d["_id"]
        if not withid and "id" in d:
            del d["id"]
        if withid and self.id is not None:
            d["_id"] = self.id
        return d

    class Config:
        '''UserApiTrxSchema config'''
        validate_assignment = True
        validate_all = False


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
    """User login schema"""
    username: str
    password: str


class UserApiEmailSchema(BaseModel):
    """Basic Schema to receive an email element"""
    email: str
    apitoken: str


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
    # pylint: disable = line-too-long
    description: Annotated[constr(strip_whitespace=True, min_length=0, max_length=500), Optional[str]] = Field(default=None, description="Description")  # type: ignore # noqa: E501
    target: Optional[str] = None
    origen: Optional[str] = None
    currency: Optional[str] = None
    method: Optional[str] = None
    channel: Optional[str] = None
    token: Optional[str] = None
    checksum: Optional[str] = None

    _description_val_unsafe = unsafe_validator('description')
    _description_val_lowercase = lowercase_validator('description')


class TrxUpdateBaseSchema(BaseModel):
    """Base schema for transaction updates"""
    id: Optional[str] = None
    status: str
    # pylint: disable = line-too-long
    descriptor: Annotated[constr(strip_whitespace=True, min_length=0, max_length=1000), Optional[str]] = Field(default=None, description="Transaction descriptor")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    reference: Annotated[constr(strip_whitespace=True, min_length=0, max_length=500), Optional[str]] = Field(default=None, description="Transaction reference")  # type: ignore # noqa: E501
    # pylint: disable = line-too-long
    reason: Annotated[constr(strip_whitespace=True, min_length=0, max_length=500), Optional[str]] = Field(default=None, description="Transaction reason")  # type: ignore # noqa: E501

    _descriptor_val_unsafe = unsafe_validator('descriptor')
    _descriptor_val_lowercase = lowercase_validator('descriptor')
    _reference_val_unsafe = unsafe_validator('reference')
    _reference_val_lowercase = lowercase_validator('reference')
    _reason_val_unsafe = unsafe_validator('reason')
    _reason_val_lowercase = lowercase_validator('reason')


class TrxUpdateSchema(TrxUpdateBaseSchema):
    """Schema for transaction updates"""
    username: Optional[str] = None
    merchant: Optional[str] = None
    by_merchant: Optional[str] = None
    created: int = Field(default_factory=lambda: int(
        datetime.now().strftime('%Y%m%d%H%M%S')))
    createds: float = Field(default_factory=time.time)
    modifieds: float = Field(default_factory=time.time)
    completed: bool = False
    transaction: Optional[TrxUpdateExtraBaseSchema] = None

    class Config:  # pylint: disable= missing-class-docstring
        orm_mode = True

    def to_dict(self):
        """Convert TrxUpdateSchema to dict"""
        data = self.model_dump(exclude_none=True)
        if self.transaction:
            data['transaction'] = self.transaction.model_dump(
                exclude_none=True)
        return data


class MessageUser(BaseModel):
    """Message user schema"""
    id: str = ""
    access_token: str = None


class TrxHeadEcheck(BaseModel):
    """Transaction head for echeck"""
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
    sum: Optional[float] = 0
    createds: Optional[float] = 0
    modifieds: Optional[float] = 0
    created: Optional[int] = 0
    modified: Optional[int] = 0

    def to_dict(self, withid: bool = True):
        """convert to dict"""
        d = self.model_dump(exclude_none=False)
        if not withid and "_id" in d:
            del d["_id"]
        if not withid and "id" in d:
            del d["id"]
        if withid and self.id is not None:
            d["_id"] = self.id
        return d


class TrxHeadEcheckList:
    """List of transaction heads for echeck"""
    list: List[TrxHeadEcheck]


# class PullTrxEcheck(BaseModel):
#    """Core Transaction Data"""
#    customeraccount: Optional[str] = None
#    amount: Optional[float] = None
#    cxname: Optional[str] = None
#    routing: Optional[str] = None
#    bankaccount: Optional[str] = None
#    accounttype: Optional[str] = None
#    email: Optional[str] = None
#    address: Optional[str] = None
#    trxtype: Optional[str] = None

# pylint:disable=pointless-string-statement, syntax-error
# class TrxRowEcheck(PullTrxEcheck):
#    fees: float = 0
#    origen: Optional[str] = None
#    currency: Optional[str] = None
#    parent: Optional[str] = None
#    tXyXpXe: sXtXr = "row"
#    method: Optional[str] = None
#    created: int = 0
#    modified: int = 0
#    createds: float = 0
#    modifieds: float = 0
#    merchant: Optional[str] = None
#    status: str = "pending"
#    descriptor: Optional[str] = None
#    reference: Optional[str] = None
#    reason: Optional[str] = None
#    comment: Optional[str] = None
#
#    def to_dict(self):
#        return self.model_dump(exclude_none=True)


class TrxRowEcheck(UserApiTrxSchema):
    '''Generic Transaction Echeck'''
    class Config:
        '''UserApiTrxSchema config'''
        validate_assignment = True
        validate_all = False


class TrxRowEcheckId(UserApiTrxSchema):
    '''Generic Transaction Echeck'''


class TrxRowEcheckSignature(BaseModel):
    '''This is for the Total line in the files'''
    label: Optional[str] = None
    total: Optional[float] = 0.0
    count: Optional[int] = 0


class TrxRowEcheckList:
    """An array of Echeck rows"""
    list: List[TrxRowEcheck]

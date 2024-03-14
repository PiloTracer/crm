"""class description"""
from datetime import datetime
import time
from typing import Optional, List
from pydantic import BaseModel, Field, validator, ValidationError

from config.netcashach_config import LENGTHS, REGEXES


class UserApiTrxSchema(BaseModel):
    """Basic Schema to receive a new Transaction via API"""
    id: Optional[str] = Field(None, alias='_id')
    authchecksum: Optional[str] = None
    authemail: Optional[str] = None
    customeraccount: str
    amount: float
    currency: str
    fees: float = 0
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
    version: str = "0"
    apikey: Optional[str] = None
    origen: Optional[str] = None
    created_by: Optional[str] = None
    created_merchant: Optional[str] = None

    @validator('authemail', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_authemail(cls, value):
        '''Convert authemail to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('authemail')
    # pylint: disable = no-self-argument
    def validate_authemail(cls, value):
        '''Validate Authenticate Email'''
        if value is not None:
            if not REGEXES["email"].match(value):
                raise ValidationError('Invalid authemail')
            if len(value) > LENGTHS["email"]:
                raise ValidationError(
                    f'authemail must be less than {
                        LENGTHS["email"]} characters')
        return value

    @validator('customeraccount', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_customeraccount(cls, value):
        '''Convert customeraccount to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('customeraccount')
    # pylint: disable = no-self-argument
    def validate_customeraccount(cls, value):
        '''Validate Customer Account'''
        if value is not None:
            if not REGEXES["customeraccount"].match(value):
                raise ValidationError('Invalid customeraccount')
            if len(value) > LENGTHS["customeraccount"]:
                raise ValidationError(
                    f'customeraccount must be less than {
                        LENGTHS["customeraccount"]} characters')
        return value

    @validator('amount')
    # pylint: disable = no-self-argument
    def validate_amount(cls, value):
        '''Validate Amount'''
        if value is not None:
            if not REGEXES["amount"].match(str(value)):
                raise ValidationError('Invalid amount')
            if len(str(value)) > LENGTHS["cxname"]:
                raise ValidationError(
                    f'amount must be less than {
                        LENGTHS["amount"]} characters')
        return value

    @validator('cxname', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_cxname(cls, value):
        '''Convert cxname to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('cxname')
    # pylint: disable = no-self-argument
    def validate_cxname(cls, value):
        '''Validate Customer Name'''
        if value is not None:
            if not REGEXES["cxname"].match(value):
                raise ValidationError('Invalid cxname')
            if len(value) > LENGTHS["cxname"]:
                raise ValidationError(
                    f'cxname must be less than {
                        LENGTHS["cxname"]} characters')
        return value

    @validator('routing', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_routing(cls, value):
        '''Convert routing to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('routing')
    # pylint: disable = no-self-argument
    def validate_routing(cls, value):
        '''Validate routing'''
        if value is not None:
            if not REGEXES["routing"].match(value):
                raise ValidationError('Invalid routing')
            if len(value) > LENGTHS["routing"]:
                raise ValidationError(
                    f'routing must be less than {
                        LENGTHS["routing"]} characters')
        return value

    @validator('bankaccount', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_bankaccount(cls, value):
        '''Convert bankaccount to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('bankaccount')
    # pylint: disable = no-self-argument
    def validate_bankaccount(cls, value):
        '''Validate bankaccount number'''
        if value is not None:
            if not REGEXES["bankaccount"].match(value):
                raise ValidationError('Invalid bankaccount')
            if len(value) > LENGTHS["bankaccount"]:
                raise ValidationError(
                    f'bankaccount must be less than {
                        LENGTHS["bankaccount"]} characters')
        return value

    @validator('accounttype', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_accounttype(cls, value):
        '''Convert accounttype to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('accounttype')
    # pylint: disable = no-self-argument
    def validate_accounttype(cls, value):
        '''Validate accounttype'''
        if value is not None:
            if not REGEXES["accounttype"].match(value):
                raise ValidationError('Invalid accounttype')
            if len(value) > LENGTHS["accounttype"]:
                raise ValidationError(
                    f'accounttype must be less than {
                        LENGTHS["accounttype"]} characters')
        return value

    @validator('email', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_email(cls, value):
        '''Convert email to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('email')
    # pylint: disable = no-self-argument
    def validate_email(cls, value):
        '''Validate email'''
        if value is not None:
            if not REGEXES["email"].match(value):
                raise ValidationError('Invalid email')
            if len(value) > LENGTHS["email"]:
                raise ValidationError(
                    f'email must be less than {
                        LENGTHS["email"]} characters')
        return value

    @validator('address', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_address(cls, value):
        '''Convert address to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('address')
    # pylint: disable = no-self-argument
    def validate_address(cls, value):
        '''Validate address'''
        if value is not None:
            if not REGEXES["address"].match(value):
                raise ValidationError('Invalid address')
            if len(value) > LENGTHS["address"]:
                raise ValidationError(
                    f'address must be less than {
                        LENGTHS["address"]} characters')
        return value

    @validator('trxtype', pre=True)
    # pylint: disable = no-self-argument
    def lowercase_trxtype(cls, value):
        '''Convert trxtype to lowercase'''
        if value is not None:
            value = value.lower()
        return value

    @validator('trxtype')
    # pylint: disable = no-self-argument
    def validate_trxtype(cls, value):
        '''Validate trxtype'''
        if value is not None:
            if not REGEXES["trxtype"].match(value):
                raise ValidationError('Invalid trxtype')
            if len(value) > LENGTHS["trxtype"]:
                raise ValidationError(
                    f'trxtype must be less than {
                        LENGTHS["trxtype"]} characters')
        return value

    class Config:  # pylint: disable= missing-class-docstring
        validate_assignment = True
        allow_population_by_field_name = True

    def to_dict(self):
        """convert to dict"""
        return self.model_dump(by_alias=True, exclude_none=True)


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
    description: Optional[str] = None
    target: Optional[str] = None
    origen: Optional[str] = None
    currency: Optional[str] = None
    method: Optional[str] = None
    channel: Optional[str] = None
    token: Optional[str] = None
    checksum: Optional[str] = None


class TrxUpdateBaseSchema(BaseModel):
    """Base schema for transaction updates"""
    id: Optional[str] = None
    status: str
    descriptor: Optional[str] = None
    reference: Optional[str] = None
    reason: Optional[str] = None


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

    def to_dict(self):
        """convert to dict"""
        return self.model_dump(exclude_none=True)


class TrxHeadEcheckList:
    """List of transaction heads for echeck"""
    list: List[TrxHeadEcheck]


class PullTrxEcheck(BaseModel):
    """Core Transaction Data"""
    customeraccount: Optional[str] = None
    amount: Optional[float] = None
    cxname: Optional[str] = None
    routing: Optional[str] = None
    bankaccount: Optional[str] = None
    accounttype: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    trxtype: Optional[str] = None
    fees: float = 0
    origen: Optional[str] = None
    currency: Optional[str] = None

    @validator('customeraccount')
    def validate_customeraccount(cls, value):  # pylint: disable = no-self-argument # noqa: E501
        '''Validate Customer Account'''
        if value is not None:
            if not REGEXES["customeraccount"].match(value):
                raise ValidationError('Invalid customeraccount')
            if len(value) > LENGTHS["customeraccount"]:
                raise ValidationError(
                    f'customeraccount must be less than {
                        LENGTHS["customeraccount"]} characters')  # noqa: E501 #pylint: disable= line-too-long
        return value


class TrxRowEcheck(PullTrxEcheck):
    """Transaction row for echeck"""
    parent: Optional[str] = None
    type: str = "row"
    method: Optional[str] = None
    created: int = 0
    modified: int = 0
    createds: float = 0
    modifieds: float = 0
    merchant: Optional[str] = None
    status: str = "pending"
    descriptor: Optional[str] = None
    reference: Optional[str] = None
    reason: Optional[str] = None
    comment: Optional[str] = None

    def to_dict(self):
        """convert to dict"""
        return self.model_dump(exclude_none=True)


class TrxRowEcheckSignature(BaseModel):
    '''This is for the Total line in the files'''
    label: Optional[str] = None
    total: Optional[float] = 0.0
    count: Optional[int] = 0


class TrxRowEcheckId(TrxRowEcheck):
    """Transaction row for echeck with id"""
    id: Optional[str] = None

    def to_dict(self, withid: bool = True):
        """convert to dict"""
        d = self.model_dump(exclude_none=True)
        if withid and self.id is not None:
            d["_id"] = self.id
        return d


class TrxRowEcheckList:
    """An array of Echeck rows"""
    list: List[TrxRowEcheck]

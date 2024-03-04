"""class description"""
# from datetime import datetime
import time
from pydantic import BaseModel, Field


class MerchProcessorModel(BaseModel):
    """docstring"""
    id: str = Field(None, alias='_id')
    createdby: str = None
    createds: float = Field(default_factory=time.time)
    merchant: str = None
    processor: str = None
    family: str = None
    type: str = None
    active: bool = True
    modifieds: float = createds

    def to_dict(self):
        """convert to dict"""
        return {
            '_id': self.id,
            'createdby': self.createdby,
            'createds': self.createds,
            'merchant': self.merchant,
            'processor': self.processor,
            'family': self.family,
            'type': self.type,
            'active': self.active,
            'modifieds': self.modifieds
        }


class MerchRangeModel(BaseModel):
    """docstring"""
    over: float = 0
    to: float = 0
    rate: float = 0
    flat: float = 0

    def to_dict(self):
        """convert to dict"""
        return {
            'over': self.over,
            'to': self.to,
            'rate': self.rate,
            'flat': self.flat
        }


class MerchFeeModel(BaseModel):
    """docstring"""
    id: str = Field(None, alias='_id')
    rev: str = Field(None, alias='_rev')
    createdby: str = None
    processor_id: str = None
    createds: float = Field(default_factory=time.time)
    merchant: str = None
    processor: str = None
    type: str = "f"
    active: bool = True
    ftype: str = None
    fname: str = None
    val: float = 0
    range: MerchRangeModel = MerchRangeModel()

    def to_dict(self):
        """convert to dict"""
        return {
            '_id': self.id,
            '_rev': self.rev,
            'createdby': self.createdby,
            'processor_id': self.processor_id,
            'createds': self.createds,
            'merchant': self.merchant,
            'processor': self.processor,
            'type': self.type,
            'active': self.active,
            'ftype': self.ftype,
            'fname': self.fname,
            'val': self.val,
            'range': self.range.to_dict()
        }


class MerchModel(BaseModel):
    """docstring"""
    id: str = Field(None, alias='_id')
    rev: str = Field(None, alias='_rev')
    email: str = None
    type: str = None
    active: bool = False
    createds: float = 0
    modifieds: float = 0

    def to_dict(self):
        """convert to dict"""
        return {
            '_id': self.id,
            'email': self.email,
            'type': self.type,
            'active': self.active,
            'createds': self.createds,
            'modifieds': self.modifieds
        }

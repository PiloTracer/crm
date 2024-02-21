"""class description"""
# from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MerchProcessorModel(BaseModel):
    """docstring"""
    _id: str = None
    _rev: Optional[str] = None
    id: str = None
    createdby: str = None
    created: float = 0
    merchant: str = None
    processor: str = None
    family: str = None
    type: str = None
    active: bool = True

    def to_dict(self):
        """convert to dict"""
        return {
            '_id': self._id if self._id and self._id is not None and self._id != "" else self.id,
            'createdby': self.createdby,
            'created': self.created,
            'merchant': self.merchant,
            'processor': self.processor,
            'family': self.family,
            'type': self.type,
            'active': self.active
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
    _id: str = None
    _rev: Optional[str] = None
    id: str = None
    createdby: str = None
    processor_id: str = None
    created: float
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
            '_id': self._id if self._id and self._id is not None and self._id != "" else self.id,
            'createdby': self.createdby,
            'processor_id': self.processor_id,
            'created': self.created,
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
    _id: str = None
    _rev: Optional[str] = None
    id: str = None
    email: str = None
    type: str = None
    active: bool = False

    def __init__(
        self,
        _id="",  # pylint: disable=redefined-builtin
        _rev: Optional[str] = None,
        id=None,  # pylint: disable=redefined-builtin
        email=None,
        type=None,  # pylint: disable=redefined-builtin
        active=False  # pylint: disable=redefined-builtin
    ):
        super().__init__()
        self._id: str = _id
        self._rev: Optional[str] = _rev,
        self.id: str = id
        self.email: str = email
        self.type: str = type
        self.active: bool = active

    def to_dict(self):
        """convert to dict"""
        return {
            '_id': self._id,
            'id': self.id,
            'email': self.email,
            'type': self.type,
            'active': self.active
        }

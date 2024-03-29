'''General Helper Models'''
from datetime import datetime
import time
from typing import List, Optional
from pydantic import BaseModel, Field


class LogTrxModel(BaseModel):
    """Class representing a class of ransaction Log entry"""
    id: str = Field(None, alias='_id')
    created: int = \
        Field(default_factory=lambda: int(
            datetime.now().strftime('%Y%m%d%H%M%S')))
    createds: float = Field(default_factory=time.time)
    modifieds: float = Field(default_factory=time.time)
    merchant: Optional[str] = None
    created_merchant: Optional[str] = None
    created_by: Optional[str] = None
    message: Optional[str] = None
    partdate: Optional[int] = 0
    doc_id: Optional[str] = None
    parent: Optional[str] = None
    filename: Optional[str] = None
    status: Optional[bool] = False
    src: Optional[str] = None
    extra: Optional[List[str]] = None  # New dictionary attribute

    def to_dict(self):
        """convert to dict"""
        # Convert the object to a dictionary for storing in CouchDB
        return {
            '_id': str(self.id),
            'created': self.created,
            'createds': self.createds,
            'modifieds': self.modifieds,
            'created_merchant': self.created_merchant,
            'created_by': self.created_by,
            'merchant': self.merchant,
            'message': self.message,
            'partdate': self.partdate,
            'doc_id': self.doc_id,
            'parent': self.parent,
            'filename': self.filename,
            'status': self.status,
            'src': self.src,
            'extra': self.extra
        }

    @classmethod
    def from_dict(cls, data):
        """parse"""
        # Create an object from a dictionary retrieved from CouchDB
        return cls(
            id=data._id,  # pylint:disable=protected-access
            created=data.get('created'),
            createds=data.get('createds'),
            modifieds=data.get('modifieds'),
            created_merchant=data.get('created_merchant'),
            created_by=data.get('created_by'),
            merchant=data.get('merchant'),
            message=data.get('message'),
            partdate=data.get('partdate'),
            doc_id=data.get('doc_id'),
            parent=data.get('parent'),
            filename=data.get('filename'),
            status=data.get('status'),
            src=data.get('src'),
            extra=data.get('extra')
        )

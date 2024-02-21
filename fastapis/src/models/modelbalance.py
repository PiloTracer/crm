"""class description"""
# from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BalanceCreatedModel(BaseModel):
    """Creation data for Balance Trx"""
    id: str | None = ""
    merchant: str | None = ""
    created: float = 0
    createdf: int = 0


class BalanceTrxStatusModel(BaseModel):
    """Status for Balance Trx"""
    status: str | None = ""  # [P]ending, [C]ompleted, or [F]ailed.
    detail: str | None = ""
    amntsign: float = 0
    feesign: float = 0
    tot: float = 0
    totsign: float = 0


class BalanceTrxMerchantModel(BaseModel):
    """Merchant data for Balance Trx"""
    merchant: str | None = ""  # the merchant to which the transaction belongs
    id: str | None = ""
    customer: str | None = ""
    bank_name: str | None = ""
    branch: str | None = ""


class BalanceModel(BaseModel):
    """docstring"""
    id: str | None = ""  # unique transaction dentifier.
    created: BalanceCreatedModel = BalanceCreatedModel()
    status: BalanceTrxStatusModel = BalanceTrxStatusModel()
    merchant: BalanceTrxMerchantModel = BalanceTrxMerchantModel()
    type: str | None = ""  # [C]redit or [D]ebit.
    # [A]djustment or [F]unding or [P]ayment or [R]eversal.
    context: str | None = ""
    trxtype: str | None = ""
    amnt: float = 0  # Monetary value.
    fee: float = 0  # Any fees associated with the transaction.
    description: str | None = ""  # A brief description for the transaction.
    reference: str | None = ""
    currency: str | None = ""
    exrate: float = 0  # The currency in which the transaction is conducted.
    method: str | None = ""  # [in-person], [online], [ATM]
    channel: str | None = ""
    token: str | None = ""
    checksum: str | None = ""
    reversed: Optional[bool] = False
    message: str | None = ""
    origen: str | None = None

    def to_dict_noid(self):
        """convert to dict"""
        return {
            'created': self.created.__dict__,
            'status': self.status.__dict__,
            'merchant': self.merchant.__dict__,
            'type': self.type,
            'context': self.context,
            'trxtype': self.trxtype,
            'amnt': self.amnt,
            'fee': self.fee,
            'method': self.method,
            'description': self.description,
            'reference': self.reference,
            'currency': self.currency,
            'exrate': self.exrate,
            'channel': self.channel,
            'reversed': self.reversed,
            'message': self.message,
            'origen': self.origen
        }

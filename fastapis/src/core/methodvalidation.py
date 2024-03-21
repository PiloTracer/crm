'''Settings management classes'''
import os
from dotenv import load_dotenv
load_dotenv("../.env.methods")


class NetCashACH():  # pylint: disable=too-few-public-methods
    '''Definition for Net Cash ACH'''
    header: str = os.getenv("netcashach_header")
    cols: str = os.getenv("netcashach_cols")
    re_customerid: str = os.getenv("netcashach_regex_customer_id")
    re_amount: str = os.getenv("netcashach_regex_amount")
    re_name: str = os.getenv("netcashach_regex_name")
    re_bankrouting: str = os.getenv("netcashach_regex_bankrouting")
    re_bankaccount: str = os.getenv("netcashach_regex_bankaccount")
    re_accounttype: str = os.getenv("netcashach_regex_accounttype")
    re_email: str = os.getenv("netcashach_regex_email")
    re_address: str = os.getenv("netcashach_regex_address")
    re_transactiontype: str = os.getenv("netcashach_regex_transactiontype")

# myconfig.py
import re

HEADER = "customeraccount|amount|cxname|routing|bankaccount|" + \
    "accounttype|email|address|trxtype|parent"
COLS = 9
SHEETNAME = "E-Check"
IGNORE_COL = -1
IGNORE_COL_VAL = "total"
IGNORE_LAST_ROWS = 1
IGNORE_LAST_COLS = 0
BIG_COLS = ["address", "cxname"]

REGEXES = {
    "customeraccount": re.compile(r'^[a-z0-9]{3,20}$', re.IGNORECASE),
    "amount": re.compile(r'^\d+\.\d+$', re.IGNORECASE),
    # Applying big field validation instead, following pattern will be ignored
    "cxname": re.compile(r'^[a-z\'\., -]+(?: [a-z\'\., -]+)*$', re.IGNORECASE),
    "routing": re.compile(r'^\d{5,20}$', re.IGNORECASE),
    "bankaccount": re.compile(r'^[a-z 0-9-]{6,50}$', re.IGNORECASE),
    "accounttype": re.compile(r'^[a-z]$', re.IGNORECASE),
    "email": re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
                        re.IGNORECASE),
    # Applying big field validation instead, following pattern will be ignored
    "address": re.compile(r'^[#0-9a-z\s,.\'-]+$', re.IGNORECASE),
    "trxtype": re.compile(r'^(payout|inflow)$', re.IGNORECASE),
    "applytoall": re.compile(r'[^@<>\(\)\[\]|_\"]', re.IGNORECASE)  # not used
}

LENGTHS = {
    "customeraccount": 20,
    "amount": 20,
    "cxname": 100,
    "routing": 20,
    "bankaccount": 50,
    "accounttype": 1,
    "email": 100,
    "address": 200,
    "trxtype": 25
}


def get_max_len(col):
    '''Get the max length for a given col'''
    if LENGTHS and col in LENGTHS:
        return LENGTHS[col]
    return 10000

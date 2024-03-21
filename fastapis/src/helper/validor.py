'''General Validator Functions'''
import re
from typing import Dict
from pydantic import validator

REGEXES = {
    "email": re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
                        re.IGNORECASE),
    "regularalphanumeric": re.compile(r'^[a-z0-9-_.]*$', re.IGNORECASE),
    "amount": re.compile(r'^\d+(\.\d+)?$', re.IGNORECASE),
    "name": re.compile(r'^[a-z0-9À-ÿ\'\., -]+(?: [a-z0-9À-ÿ\'\., -]+)*$', re.IGNORECASE),  # noqa: E501
    "digits": re.compile(r'^\d*$'),
    "bankaccount": re.compile(r'^[a-z 0-9-]*$', re.IGNORECASE),
    "letters": re.compile(r'^[a-z]*$'),
    "alpha": re.compile(r'^[a-zA-ZÀ-ÿ]*$', re.UNICODE),
    "trxtype": re.compile(r'^(payout|inflow)$', re.IGNORECASE),
    "currency": re.compile(r'^(usd|eur)$', re.IGNORECASE)
}

LENGTHS = {
    "email": 100,
    "regularsize": 50,
    "amount": 20,
    "name": 100,
    "digitsregularsize": 20,
    "bankaccount": 50
}

UNSAFE_PATTERNS = {
    # pylint: disable=line-too-long
    "script": re.compile(r'<script[^>]*>([^<]*)</script>', re.IGNORECASE),
    # pylint: disable=line-too-long
    "xss": re.compile(r'''(<script[^>]*>([^<]*)</script>|javascript:[^ ]+)''', re.IGNORECASE),  # noqa: E501
    # pylint: disable=line-too-long
    # SQL injection patterns
    "command": re.compile(r'(\bbash\b|\bsh\b|\bcmd\b|\bpowershell\b|\bperl\b|\bphp\b|\.\./|[|&;]|(?<![a-zA-Z0-9])`(?![a-zA-Z0-9])|(?<![a-zA-Z0-9])"(?![a-zA-Z0-9]))', re.IGNORECASE),
    "sql": re.compile(r"(?:\b(SELECT|INSERT|UPDATE|DELETE|EXECUTE|EXEC|DROP|ALTER|CREATE|SHOW TABLES|SHOW DATABASES)\b)", re.IGNORECASE),  # noqa: E501
    # File inclusion and path traversal patterns
    "file_inclusion": re.compile(r'(\.{2,}|[a-zA-Z]:\\|(?:%2e){2}|(?:%2f))', re.IGNORECASE),  # noqa: E501
    # XML and XPATH injection patterns
    "xml_injection": re.compile(r'<!\[CDATA|<\?xml|xmlns\=|<!DOCTYPE|\]\]>', re.IGNORECASE),  # noqa: E501
    # HTTP response splitting patterns
    "http_response_splitting": re.compile(r'(\r\n|\r|\n)(content-type:|set-cookie:|location:)', re.IGNORECASE)  # noqa: E501
}


def length_validator(max_length: int):
    '''Validates the length of the value'''
    def validate(value):
        if len(str(value)) > max_length:
            raise ValueError(f'Value must be less than {
                             max_length} characters')
        return value
    return validator('length', allow_reuse=True)(validate)


def lowercase_validator(field: str):
    '''Convert value to lowercase'''
    def validate(value):
        if value is not None:
            value = value.lower()
        return value
    return validator(field, allow_reuse=True, pre=True)(validate)


def unsafe_validator(  # pylint: disable = dangerous-default-value
        field: str, patterns: Dict[str, re.Pattern] = UNSAFE_PATTERNS):
    '''Validates the field value against unsafe patterns'''
    def validate(value):
        i = 0
        for pattern_name, pattern in patterns.items():
            if pattern.search(str(value)):
                raise ValueError(f'Unsafe {
                    pattern_name} pattern found in {field} ({i})')
            i += 1
        return value
    return validator(field, allow_reuse=True)(validate)


def email_validator(field: str):
    '''Validates email using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["email"].match(str(value)):
                raise ValueError(f'Invalid {field}')
            if len(str(value)) > LENGTHS["email"]:
                raise ValueError(
                    f'{field} must be less than {
                        LENGTHS["email"]} characters')
        return value
    return validator(field, allow_reuse=True)(validate)


def regular_alphanumeric_validator(field: str):
    '''Validates regular size alphanumeric strings w/ REGEX'''
    def validate(value):
        if value is not None and value != "":
            if not REGEXES["regularalphanumeric"].match(str(value)):
                raise ValueError(f'Invalid {field}')
            if len(str(value)) > LENGTHS["regularsize"]:
                raise ValueError(
                    f'{field} must be less than {
                        LENGTHS["regularsize"]} characters')
        return value
    return validator(field, allow_reuse=True)(validate)


def amount_validator(field: str):
    '''Validates Amount using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["amount"].match(str(value)):
                raise ValueError(f'Invalid {field}')
            if len(str(value)) > LENGTHS["amount"]:
                raise ValueError(
                    f'{field} must be less than {
                        LENGTHS["amount"]} characters')
        return value
    return validator(field, allow_reuse=True)(validate)


def name_validator(field: str):
    '''Validates Name using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["name"].match(str(value)):
                raise ValueError(f'Invalid {field}')
            if len(str(value)) > LENGTHS["name"]:
                raise ValueError(
                    f'{field} must be less than {
                        LENGTHS["name"]} characters')
        return value
    return validator(field, allow_reuse=True)(validate)


def digits_validator(field: str):
    '''Validates Numeric fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["digits"].match(str(value)):
                raise ValueError(f'Invalid {field}')
            if len(str(value)) > LENGTHS["digitsregularsize"]:
                raise ValueError(
                    f'{field} must be less than {
                        LENGTHS["digitsregularsize"]} characters')
        return value
    return validator(field, allow_reuse=True)(validate)


def bankaccount_validator(field: str):
    '''Validates Bank Account fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["bankaccount"].match(str(value)):
                raise ValueError(f'Invalid {field}')
        return value
    return validator(field, allow_reuse=True)(validate)


def letters_validator(field: str):
    '''Validates Numeric fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["letters"].match(str(value)):
                raise ValueError(f'Invalid {field}')
        return value
    return validator(field, allow_reuse=True)(validate)


def alpha_validator(field: str):
    '''Validates Numeric fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["alpha"].match(str(value)):
                raise ValueError(f'Invalid {field}')
        return value
    return validator(field, allow_reuse=True)(validate)


def trxtype_validator(field: str):
    '''Validates Numeric fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["trxtype"].match(str(value)):
                raise ValueError(f'Invalid {field}')
        return value
    return validator(field, allow_reuse=True)(validate)


def currency_validator(field: str):
    '''Validates Numeric fields using REGEX'''
    def validate(value):
        if value is not None:
            if not REGEXES["currency"].match(str(value)):
                raise ValueError(f'Invalid {field}')
        return value
    return validator(field, allow_reuse=True)(validate)

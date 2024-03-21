'''Redis counter generation'''
import redis


redis_client = redis.Redis(host='10.5.0.4', port=6379, db=0)
char_set = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
base = len(char_set)


def counter_next(countid: str) -> int:
    '''Counter increment'''
    # Increment and retrieve the counter value
    counter_value = redis_client.incr(countid)
    if counter_value > 56800235583:
        redis_client.set(countid, 0)
    return int(counter_value)


def counter_next_leading_0(countid: str) -> str:
    '''Counter increment with leading 0s'''
    # Increment and retrieve the counter value
    counter_value = counter_next(countid)
    return str(counter_value).zfill(10)


def num_to_alphanumeric(number="0", countid: str = "general") -> str:
    '''Convert number to 6-char long alphanumeric'''
    number = str(number).strip()
    # examples:
    # 1           : "000001"
    # 1000000     : "00Q0SG"
    # 1000001     : "00Q0SH"
    # 10000000    : "00VWGX"
    # 56800235583 : "zzzzzz"
    if number.isnumeric() is False:
        if number is not "":
            return number
        else:
            number = "0"

    number = abs(int(number))

    if number == 0:
        number = counter_next(countid)

    # Convert the number to alphanumeric representation
    result = ""
    while number > 0:
        number, remainder = divmod(number, base)
        result = char_set[remainder] + result

    # Pad the result with leading zeros to ensure a consistent length of 6 characters
    result = result.zfill(6)

    return result


def alphanumeric_to_num(alphanumeric: str) -> int:
    '''Convert alphanumeric to number'''

    # Remove leading zeros from the alphanumeric string
    alphanumeric = alphanumeric.lstrip('0')

    # Convert the alphanumeric string to a number
    number = 0
    for char in alphanumeric:
        number = number * base + char_set.index(char)

    return number

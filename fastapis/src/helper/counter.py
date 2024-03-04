'''Redis counter generation'''
import redis


redis_client = redis.Redis(host='10.5.0.4', port=6379, db=0)


def counter_next(countid: str) -> int:
    '''Counter increment'''
    # Increment and retrieve the counter value
    counter_value = redis_client.incr(countid)
    if counter_value > 1000000000:
        redis_client.set(countid, 0)
    return int(counter_value)


def counter_next_leading_0(countid: str) -> str:
    '''Counter increment with leading 0s'''
    # Increment and retrieve the counter value
    counter_value = counter_next(countid)
    return str(counter_value).zfill(10)

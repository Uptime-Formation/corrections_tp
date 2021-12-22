from .monster_icon import *
import redis



def test_redis_counter():
    redis_cache = redis.StrictRedis(host='redis', port=6379, socket_connect_timeout=2, socket_timeout=2, db=0)

    result = redis_visits_counter(redis_cache)

    assert result
    assert not isinstance(result, redis.RedisError)
    assert isinstance(result, int)

    result2 = redis_visits_counter(redis_cache)

    assert result2 == result + 1

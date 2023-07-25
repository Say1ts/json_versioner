import redis
from database.connection import get_redis_cfg


def generate_vid():
    with redis.Redis(**get_redis_cfg()) as r:
        with r.pipeline() as pipe:
            pipe.multi()
            pipe.incr('vid')
            pipe.get('vid')
            result = pipe.execute()
            return result[0]


def generate_id():
    with redis.Redis(**get_redis_cfg()) as r:
        with r.pipeline() as pipe:
            pipe.multi()
            pipe.incr('id')
            pipe.get('id')
            result = pipe.execute()
            return result[0]


def reset_counter():
    # Connect to Redis
    with redis.Redis(**get_redis_cfg()) as r:
        counter_key = 'id'
        r.set(counter_key, 0)
        counter_key = 'vid'
        r.set(counter_key, 0)

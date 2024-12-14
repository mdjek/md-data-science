import redis
import json
from constants import REDIS_URL


def get_keys_to_str(item, keys) -> str:
    result_str = ""

    for index in range(len(keys)):
        result_str += f"{item.__dict__[keys[index]]}{'' if (len(keys) - 1) == index else ':'}"

    return result_str


def connect_redis():
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        return redis_client

    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None


def set_item_redis(redis_client, item, key_prefix, keys):
    item_json = dict()

    for k in item.__dict__:
        if k != "_sa_instance_state":
            item_json[k] = item.__dict__[k]

    keys_str = get_keys_to_str(item, keys)

    if item:
        redis_key = f"{key_prefix}:{keys_str}"

        # redis_client.hset(redis_key, mapping=json.dumps(item_json))

        redis_client.set(redis_key, json.dumps(item_json), ex=180)
        pass
    else:
        print("Data inserted into Redis successfully.")
    return item


def insert_data_into_redis(data, key_prefix, keys: list):
    redis_client = connect_redis()

    try:
        if isinstance(data, list):
            for item in data:
                set_item_redis(redis_client, item, key_prefix, keys)
        else:
            set_item_redis(redis_client, data, key_prefix, keys)

    except Exception as e:
        print(f"Error inserting data into Redis: {e}")


def get_data_from_redis(cache_key) -> list:
    redis_client = connect_redis()
    keys = redis_client.keys(cache_key)
    result = []

    if keys and len(keys) == 1 and redis_client.exists(cache_key):
        cached_item = redis_client.get(cache_key)
        print("Data retrieved from cache (one item)")

        result.append(json.loads(cached_item))
    elif keys:
        for key in redis_client.keys(cache_key):
            if redis_client.exists(key):
                cached_data = redis_client.get(key)
                result.append(json.loads(cached_data))
            else:
                continue

        print("Data retrieved from cache (collection)")
    else:
        return None

    return result

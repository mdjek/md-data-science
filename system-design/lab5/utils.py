import redis
import json
from constants import REDIS_URL

# def connect_postgres(hostname, port, dbname, username, password):
#     try:
#         connection = psycopg2.connect(
#             host=hostname,
#             port=port,
#             database=dbname,
#             user=username,
#             password=password
#         )
#         return connection

#     except Exception as e:
#         print(f"Error connecting to PostgreSQL: {e}")
#         return None


# def fetch_data_from_postgres(connection, query):
#     try:
#         cursor = connection.cursor()
#         cursor.execute(query)
#         records = cursor.fetchall()
#         return records

#     except Exception as e:
#         print(f"Error fetching data from PostgreSQL: {e}")
#         return None
    

# def connect_redis(hostname, port, password=None):
def connect_redis():
    try:
        # redis_client = redis.StrictRedis(
        #     host=hostname,
        #     port=port,
        #     password=password,
        #     decode_responses=True

        # )
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        return redis_client

    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None
    
    
def set_redis_item(redis_client, item, key_prefix, keys):
    item_json = dict()

    for k in item.__dict__:
        if k != '_sa_instance_state':
            item_json[k] = item.__dict__[k]

    if item:
        redis_key = f"{key_prefix}:{item.__dict__[keys[0]]}:{item.__dict__[keys[1]]}"

        # redis_client.hset(redis_key, mapping=json.dumps(item_json))

        redis_client.set(redis_key, json.dumps(item_json), ex = 180)
        pass
    else:
        print("Data inserted into Redis successfully.")
    return item


def insert_data_into_redis(data, key_prefix, keys: list):
    redis_client = connect_redis()

    try: 
        if (isinstance(data, list)):
            for item in data:
                set_redis_item(redis_client, item, key_prefix, keys)
        else:
                set_redis_item(redis_client, data, key_prefix, keys)

    except Exception as e:
        print(f"Error inserting data into Redis: {e}")



    #     for record in data:
    #         print(record)
    #         # Assuming each record is a tuple (id, value), and you want to store it as a hash
    #         redis_key = f"{key_prefix}:{record[0]}"
    #         redis_client.hset(redis_key, mapping=record[1])

    #     print("Data inserted into Redis successfully.")

    # except Exception as e:
    #     print(f"Error inserting data into Redis: {e}")


def get_data_from_redis(cache_key) -> list:
    redis_client = connect_redis()    
    keys = redis_client.keys(cache_key)
    result = []

    # if redis_client.keys(cache_key)

    # print("````cache_key:", redis_client.keys(cache_key))

    if keys and len(keys) == 1 and redis_client.exists(cache_key):
        # print("one items")
        cached_item = redis_client.get(cache_key)
        print("Data retrieved from cache (one item)")
        result.append(json.loads(cached_item))

        # return [json.loads(result)]
    elif keys:
        # print("more items")
        # result = []

        for key in redis_client.keys(cache_key):
            if redis_client.exists(key):
                cached_data = redis_client.get(key)
                result.append(json.loads(cached_data))
            else:
                continue

        print("Data retrieved from cache (collection)")
        # return result
    else:
        return None
    
    return result

    # # scan_iter
    # if redis_client.exists(cache_key):
    #     print("redis_client.exists:", cache_key)
    #     cached_user = redis_client.get(cache_key)
    #     print("Data retrieved from cache")
    #     return json.loads(cached_user)
    # else:
    #     return None
    
    # else:
    #     data = db.query(entity_model).filter(entity_model[finded_param_key] == finded_param_value).first()

    #     if data:
    #         insert_data_into_redis(data, key_prefix, key)
    #         pass
    #     else:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     return data
    
        # return insert_data_into_redis(data, key_prefix, key)
    
        # user_json = dict()
        # for k in user.__dict__:
        #     if k != '_sa_instance_state':
        #         user_json[k] = user.__dict__[k]

        # if data:
        #     redis_client.set(cache_key, json.dumps(user_json),ex = 180)
        #     pass
        # else:
        #     raise HTTPException(status_code=404, detail="User not found")
        # return user

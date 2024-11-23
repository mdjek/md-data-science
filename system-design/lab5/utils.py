import redis
from constants import REDIS_URL

def connect_postgres(hostname, port, dbname, username, password):
    try:
        connection = psycopg2.connect(
            host=hostname,
            port=port,
            database=dbname,
            user=username,
            password=password
        )
        return connection

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def fetch_data_from_postgres(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None
    

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
    

def insert_data_into_redis(redis_client, data, key_prefix):
    try:
        for record in data:
            # Assuming each record is a tuple (id, value), and you want to store it as a hash
            redis_key = f"{key_prefix}:{record[0]}"
            redis_client.hset(redis_key, mapping=record[1])

        print("Data inserted into Redis successfully.")

    except Exception as e:
        print(f"Error inserting data into Redis: {e}")


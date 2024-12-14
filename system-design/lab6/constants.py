# Auth
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Services
POSTGRESQL_DATABASE_URL = "postgresql://postgres:pass@pgdb/profi_db"
MONGODB_URI = "mongodb://root:rootpasswd@mongo:27017/"
REDIS_URL = "redis://cache:6379/0"

KAFKA_BOOTSTRAP_SERVERS = "kafka1:9092"
KAFKA_TOPIC = "orders"
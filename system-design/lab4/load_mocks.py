from mock_loaders.load_pg_mocks import load_pg_mock_data
from mock_loaders.load_mongo_mocks import load_mongo_mock_data

# Наполняем MongoDB моками
load_mongo_mock_data()

# Наполняем Postgresql db моками
load_pg_mock_data()
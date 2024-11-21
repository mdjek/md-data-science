from fastapi import FastAPI
from routers import auth, users, orders, tasks
from load_pg_mocks import load_pg_mock_data
from load_mongo_mocks import load_mongo_mock_data

# Наполняем mongo базу моками
load_mongo_mock_data()

# Наполняем pg базу моками
# load_pg_mock_data()

# Инициализация приложения
app = FastAPI(title="App", description="API для управления заказами/услугами")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
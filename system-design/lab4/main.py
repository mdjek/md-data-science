from fastapi import FastAPI
from routers import auth, users, orders, tasks
from load_mocks import load_mock_pg_data

# Наполняем pg базу моками
# load_mock_pg_data()

# Инициализация приложения
app = FastAPI(title="App", description="API для управления заказами/услугами")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from routes import auth, user

app = FastAPI(title="App", description="API для управления заказами/услугами")

app.include_router(auth.router)
app.include_router(user.router)
# app.include_router(order.router)
# app.include_router(task.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
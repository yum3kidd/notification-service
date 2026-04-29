from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.notify import router
from app.database import engine, Base

app = FastAPI(title="Notification API Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def init_db():
    # Создаём таблицы, если их нет
    Base.metadata.create_all(bind=engine)
    # Добавляем тестовые данные
    from app.init_data import init_test_data
    init_test_data()

@app.get("/")
def root():
    return {"message": "Notification API Proxy running"}
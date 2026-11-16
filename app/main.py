from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import Base, engine
from .routers import exchange
from .scheduler import scheduler, fetch_rates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    # Загружаем курсы сразу при старте
    fetch_rates()
    # Запускаем фоновую задачу
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="Currency Exchange API", lifespan=lifespan)
app.include_router(exchange.router)
import httpx
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from . import models

def fetch_rates():
    db = SessionLocal()
    try:
        # НБРБ отдает курсы на сегодня
        res = httpx.get("https://www.nbrb.by/api/exrates/rates?periodicity=0", timeout=10)
        data = res.json()
        
        for item in data:
            code = item.get("Cur_Abbreviation")
            rate = item.get("Cur_OfficialRate")
            scale = item.get("Cur_Scale", 1)
            
            if code and rate:
                # Приводим к курсу за 1 единицу валюты
                normalized_rate = float(rate) / scale
                db.add(models.ExchangeRate(
                    currency_code=code,
                    rate=normalized_rate
                ))
        db.commit()
        print("Курсы обновлены")
    except Exception as e:
        print(f"Ошибка при загрузке курсов: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_rates, "interval", hours=24, id="fetch_rates")
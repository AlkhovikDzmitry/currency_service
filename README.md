# Currency Exchange Service

Сервис для обмена валют с автоматической загрузкой актуальных курсов с API Национального Банка Республики Беларусь (НБРБ).

## 🛠 Стек технологий
- **Python 3.11**
- **FastAPI** (веб-фреймворк)
- **PostgreSQL 15** (база данных)
- **SQLAlchemy 2.0** (ORM)
- **APScheduler** (планировщик задач для сбора курсов)
- **Docker / Docker Compose** (контейнеризация)

## 🚀 Как запустить

Для запуска потребуется установленный **Docker Desktop** (или Docker Engine + Docker Compose).

1. Клонируйте репозиторий и перейдите в папку с проектом:
   ```bash
   git clone https://github.com/AlkhovikDzmitry/currency_service
   cd currency_service
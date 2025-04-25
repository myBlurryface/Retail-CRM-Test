# API для интеграции с RetailCRM

Проект на базе FastAPI для интеграции с RetailCRM, предоставляющий эндпоинты для управления заказами, клиентами и платежами.

## Структура проекта

```
Retail-CRM-Test/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── endpoints/
│   │   ├── __init__.py    
│   │   ├── orders.py
│   │   ├── clients.py
│   │   ├── payments.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   ├── clients.py
│   │   ├── payments.py
│   ├── CRMRequests/
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   ├── clients.py
│   │   ├── payments.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
```

## Требования

- **Docker**: Установите Docker и Docker Compose ([Руководство по установке Docker](https://docs.docker.com/get-docker/)).
- **API-ключ RetailCRM**: Получите API-ключ и URL из вашего аккаунта RetailCRM (`https://yourshopname.retailcrm.ru`).

## Настройка

1. **Клонируйте репозиторий** (если применимо):
   ```bash
   git clone <repository-url>
   cd Retail-CRM-Test
   ```

2. **Настройте переменные окружения**:
   - Создайте или обновите файл `.env` в корне проекта с вашими учетными данными RetailCRM:
     ```
     RETAILCRM_API_KEY=yourapikey
     RETAILCRM_URL=https://yourshopname.retailcrm.ru/api/v5
     ```

## Запуск проекта

### Использование Docker и Docker Compose

1. **Убедитесь, что Docker запущен**:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Соберите и запустите приложение**:
   ```bash
   docker-compose up --build
   ```
   - Это соберёт Docker-образ и запустит приложение FastAPI на `http://localhost:8000`.
   - Флаг `--build` гарантирует пересборку образа с последними изменениями.

3. **Доступ к API**:
   - Swagger UI: Документация API будет доступна по адресу http://127.0.0.1:8000/api/retailcrm/docs/.
   - OpenAPI-схема: JSON-схема API будет доступна по адресу http://127.0.0.1:8000/api/retailcrm/openapi.json.
   - Пример вызова эндпоинта для создания клиента:
     ```bash
     curl -X POST "http://localhost:8000/api/clients" \
     -H "Content-Type: application/json" \
     -d '{"firstName": "Иван", "email": "ivan@example.com", "phone": "+79991234567"}'
     ```
     Ожидаемый ответ:
     ```json
     {
        "id": 62,
        "name": "Test",
        "email": "user@example.com",
        "createdAt": "2025-03-02T07:00:14"
     }
     ```

5. **Просмотр логов**:
   ```bash
   docker-compose logs
   ```

6. **Остановка приложения**:
   ```bash
   docker-compose down
   ```

## Комментарии к реализации

### Изменённые файлы
- **app/main.py**
  - Основной файл FastAPI, объединяет роутеры для заказов, клиентов и платежей.
- **app/endpoints/clients.py**
  - Реализован эндпоинты для создания клиентов и получения списка клиентов с фильтром.
- **app/CRMRequests/clients.py** 
  - Логика создания пользователя и получения списка пользователей через RetailCRM API.
- **app/schemas/clients.py** 
  - Схемы для валидации входных и выходных данных клиентов.
- **app/endpoints/orders.py**
  - Реализован эндпоинты для создания заказов и получения списка заказов для клиента.
- **app/CRMRequests/orders.py** 
  - Логика создания заказа и просмотра списка заказов пользователя через RetailCRM API.
- **app/schemas/orders.py** 
  - Схемы для валидации входных и выходных данных заказов.
- **app/endpoints/payments.py**
  - Реализован эндпоинты для создания платежей к заказам.
- **app/CRMRequests/orders.py** 
  - Логика создания платежа для заказа.
- **app/schemas/orders.py** 
  - Схемы для валидации входных и выходных данных платежа.
- **requirements.txt**
  - Включает зависимости (`fastapi`, `uvicorn`, `httpx`, `pydantic`, `python-dotenv`, и др.) с фиксированными версиями.
- **Dockerfile**
  - Настроен для `python:3.11`, устанавливает зависимости и запускает `uvicorn`.
- **docker-compose.yml**
  - Определяет сервис `web` с портом `8000` и подключением `.env`.
- **.env**
  - Хранит учетные данные RetailCRM.
- **README.md**
  - Документация на русском с инструкциями по запуску и примером вызова API.

### Основные моменты реализации
- **FastAPI приложение**:
  - RESTful API с автоматической документацией OpenAPI.
  - Модульная структура с разделением на роутеры, схемы и сервисы.
- **Интеграция с RetailCRM**:
  - Использует API v5 RetailCRM (`https://yourshopname.retailcrm.ru/api/v5`).
  - Эндпоинты для заказов, клиентов и платежей.
- **Странность с созданием заказа**:
  - Метод `POST /orders/create` ведёт себя не так, как указано в документации RetailCRM. 
    Если передать `productId` в `items`, товар не создаётся, если он не существует в справочнике, и позиция заказа может не добавиться или отобразиться некорректно. 
    Если `productId` не указан, а передан `productName`, автоматическое создание товара срабатывает, но в CRM товар отображается как `NoName`, игнорируя `productName`. 
    Для корректной работы необходимо заранее создать товар через `POST /reference/products/create` и передать его `productId` в заказе. 
    Возможное решение проблемы - проверять наличие товаров в каталоге перед отправкой запроса.
  
- **Docker**:
  - Образ на базе `python:3.11` для минимизации размера.
  - Зависимости фиксированы в `requirements.txt`.
  - `docker-compose` упрощает разработку с монтированием томов и загрузкой `.env`.

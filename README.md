Example Shared .env (./.env)

```
# .env
DEBUG=1

# RabbitMQ / Redis for Celery
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Order DB
ORDER_DB_HOST=postgres-order
ORDER_DB_NAME=order_db
ORDER_DB_USER=postgres
ORDER_DB_PASS=postgres
ORDER_DB_PORT=5432

# Inventory DB
INVENTORY_DB_HOST=postgres-inventory
INVENTORY_DB_NAME=inventory_db
INVENTORY_DB_USER=postgres
INVENTORY_DB_PASS=postgres
INVENTORY_DB_PORT=5432

# Payment DB
PAYMENT_DB_HOST=postgres-payment
PAYMENT_DB_NAME=payment_db
PAYMENT_DB_USER=postgres
PAYMENT_DB_PASS=postgres
PAYMENT_DB_PORT=5432

# Django secret (dev)
DJANGO_SECRET_KEY=devsecret

```


Example frontend .env (should be on frontend/.env)

```
VITE_ORDER_API=http://localhost:8001/api
VITE_INVENTORY_API=http://localhost:8002/api
VITE_PAYMENT_API=http://localhost:8003/api
```



* has been considered in ALLOWED_HOSTS for simplicity on dev mode


You need to create some products

which u can us the django shell

```
docker compose exec inventory python manage.py shell
```


other docker commands

```
docker compose up --build
```

```
docker compose down
```

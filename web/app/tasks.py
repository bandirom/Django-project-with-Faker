from src.celery import app

from .services import GenerateService

service = GenerateService()


@app.task()
def generate_users(amount):
    print('generate_users')
    service.add_users(n=amount)


@app.task()
def generate_transfers():
    print("generate transfers")
    service.add_transfer_day()

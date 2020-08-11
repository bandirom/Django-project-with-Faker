from random import randint, choice

import django
from faker import Faker
from datetime import timedelta, date

from .models import UserModel, Company, DateTimeModel, DataTransferModel, DataTransferManager, ResourceModel


class GenerateService:
    MIN_SIZE_B = 100
    MAX_SIZE_B = 10 ** 10
    DATE_RANGE = 180
    companies = ['Google', 'Amazon', 'Microsoft', 'SpaceX', 'IBM', 'Samsung', 'Sony', 'Foxconn',
                 'Huawei', 'Intel', 'Lenovo']
    company_size = ['mb', 'gb', 'tb']

    def __init__(self):
        self.faker = Faker()

    def get_fake_url(self):
        return self.faker.url()

    def _add_company(self):
        company_name = choice(self.companies)
        try:
            company = Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            company = Company.objects.create(name=company_name, quota=randint(50, 400), size=choice(self.company_size))
            company.save()
        return company

    def add_users(self, n=5):
        for i in range(int(n)):
            company = self._add_company()
            user = self.faker.name()
            email = self.faker.company_email()
            new_user = UserModel.objects.get_or_create(company=company, user=user, email=email)[0]
            new_user.save()

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def add_transfer_day(self):
        """Generating data for DataTransferModel
            model: DataTransferModel

        """
        start_date = date.today() - timedelta(self.DATE_RANGE)
        end_date = date.today()
        users = UserModel.objects.all().select_related('company')
        for single_date in self.daterange(start_date, end_date):
            time = DateTimeModel.objects.get_or_create(timestamp=single_date)[0]
            for user in users:
                try:
                    obj = DataTransferModel.objects.get(user=user, time=time)
                except Exception:
                    obj = DataTransferModel()
                    obj.user = user
                    obj.company = user.company
                    obj.time = time
                    bytes_size = randint(self.MIN_SIZE_B, self.MAX_SIZE_B)
                    obj.transferred_bytes = bytes_size
                    obj.size, obj.size_type = DataTransferManager.humanbytes(bytes_size)
                    obj.resource = ResourceModel.objects.get_or_create(domain=self.get_fake_url())[0]
                    obj.save()
        self.daterange(start_date, end_date)


class IndexService:

    def __init__(self):
        pass

    def get_user_list(self):
        return UserModel.objects.select_related('company').all()

    def get_user(self, _id):
        return UserModel.objects.get(id=_id).company_id

    def get_company_list(self):
        return Company.objects.all()

    def user_obj_to_json(self, obj):
        data = {
            'id': obj.id,
            'user': obj.user,
            'email': obj.email,
            'company': obj.company.name
        }
        return data

    def company_obj_to_json(self, obj) -> dict:
        return {
            'id': obj.id,
            'name': obj.name,
            'quota': obj.quota,
            'size': obj.size,
        }

    def update_user(self, data):
        obj = UserModel.objects.get(id=data['id'])
        obj.user = data['user']
        obj.email = data['email']
        obj.company_id = data['company']
        obj.save()
        return obj

    def update_company(self, data):
        obj = Company.objects.get(id=data['id'])
        obj.size = data['size']
        obj.quota = data['quota']
        obj.save()
        return obj

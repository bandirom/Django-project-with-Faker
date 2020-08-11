from django.db import models
from django.db.models.functions import ExtractYear, ExtractMonth
from django.urls import reverse

from .managers import CompanyManager, DataTransferManager


class Company(models.Model):
    name = models.CharField(max_length=100)
    quota = models.PositiveIntegerField()
    size = models.CharField(max_length=50, blank=True, null=True, choices=CompanyManager.quota_size)

    objects = CompanyManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ["-id"]


class UserModel(models.Model):
    user = models.CharField(max_length=50)
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.SET_DEFAULT, null=True, default='Self')

    def get_last_user(self):
        return UserModel.objects.last()

    def get_absolute_url(self):
        return reverse("main:user")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ["-id"]


class DateTimeModel(models.Model):
    timestamp = models.DateField(default=True)

    @staticmethod
    def get_years_months_list():
        return DateTimeModel.objects.annotate(year=ExtractYear('timestamp'),
                                              month=ExtractMonth('timestamp')).values_list('year', 'month').distinct()

    def __str__(self):
        return f'{self.timestamp}'

    class Meta:
        verbose_name = 'Date'
        verbose_name_plural = 'Dates'


class ResourceModel(models.Model):
    domain = models.URLField('Url', default='')

    def __str__(self):
        return f'{self.domain}'

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        ordering = ["-id"]


class DataTransferModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    time = models.ForeignKey(DateTimeModel, on_delete=models.CASCADE)
    transferred_bytes = models.BigIntegerField("bytes", default=100)
    size = models.FloatField("Transferred", default=100)
    size_type = models.CharField("size", max_length=50, blank=True, null=True, choices=DataTransferManager.size,
                                 default=DataTransferManager.size[0])
    resource = models.ForeignKey(ResourceModel, on_delete=models.CASCADE)

    objects = DataTransferManager()

    def __str__(self):
        return f'{self.user} - {self.company}'

    class Meta:
        verbose_name = 'Data transfer'
        verbose_name_plural = 'Data transfer'
        ordering = ["-id"]

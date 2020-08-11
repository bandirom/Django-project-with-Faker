from django.contrib import admin
from .models import Company, UserModel, DateTimeModel, ResourceModel, DataTransferModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    """Admin model for UserModel """
    list_display = ('user', 'email', 'company')
    list_filter = ('company', )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin model for Company model"""
    list_display = ('name', 'quota', 'size')
    list_filter = ('name', )


@admin.register(DateTimeModel)
class DateTimeModelAdmin(admin.ModelAdmin):
    """Admin model for Company model"""
    list_display = ('timestamp', )
    list_filter = ('timestamp', )


@admin.register(DataTransferModel)
class DataTransferModelAdmin(admin.ModelAdmin):
    """Admin model for Company model"""
    list_display = ('user', 'company', 'time', 'size', 'size_type')
    list_filter = ('user', 'company',)


@admin.register(ResourceModel)
class ResourceModelAdmin(admin.ModelAdmin):
    """Admin model for UserModel """
    list_display = ('domain',)
    list_filter = ('domain', )

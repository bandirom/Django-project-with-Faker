from django import forms
from .models import UserModel, Company


class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('user', 'email', 'company')
        fields_required = ['email', 'company']
        widgets = {
            "user": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "company": forms.Select(attrs={"class": "form-control border"}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'quota', 'size')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border", }),
            'quota': forms.NumberInput(attrs={"class": "form-control border", }),
            'size': forms.Select(attrs={"class": "form-control border", })
        }

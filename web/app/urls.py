from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import IndexView, RemoveItem, AutoGenerate, AbusersView

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('user/', IndexView.as_view(), name='user'),
    path('remove/', RemoveItem.as_view(), name='remove'),
    path('company/', IndexView.as_view(), name='company'),
    path('generate/', AutoGenerate.as_view(), name='generate_data'),
    path('abusers/', AbusersView.as_view(), name='abusers_report'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

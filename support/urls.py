from .views import bot_response
from django.urls import path


app_name = 'support'

urlpatterns = [
    path('support/', bot_response, name='support'),
]

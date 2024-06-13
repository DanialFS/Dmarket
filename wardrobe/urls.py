from django.urls import path
from . import views

app_name = 'wardrobe'

urlpatterns = [
    path('wardrobe', views.wardrobe, name='wardrobe'),
    # Add other paths here
]
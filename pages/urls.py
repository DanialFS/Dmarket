from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import render_page

app_name = 'pages'

urlpatterns = [
    path('offer', render_page, {'template_name': 'pages/offer.html'}, name='offer'),
    path('agreement', render_page, {'template_name': 'pages/agreement.html'}, name='agreement'),
    path('policy', render_page, {'template_name': 'pages/policy.html'}, name='policy'),
    path('contacts', render_page, {'template_name': 'pages/contacts.html'}, name='contacts')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
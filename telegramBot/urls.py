from django.urls import path
from telegramBot.views import *


urlpatterns = [
    path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    path('web_app/<int:chat_id>', WebApp.as_view(), name='home'),
]
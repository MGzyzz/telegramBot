import json
import requests
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from telegramBot.models import UserProfileModel
from django.conf import settings
from datetime import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)


def extract_user_data(message):
    """
    Извлекает данные пользователя из сообщения Telegram.
    
    Args:
        message (dict): Объект сообщения Telegram
        
    Returns:
        tuple: (chat_id, first_name, last_name, username, date)
    """
    chat = message.get("chat", {})
    user_from = message.get("from", {})
    
    chat_id = chat.get("id")
    first_name = user_from.get("first_name")
    last_name = user_from.get("last_name", "")
    username = user_from.get("username", "")
    
    unix_timestamp = message.get("date")
    date = timezone.make_aware(datetime.fromtimestamp(unix_timestamp)) if unix_timestamp else None
    
    return chat_id, first_name, last_name, username, date


def handle_start(message):
    
    """
    Обрабатывает команду /start: сохраняет или обновляет данные пользователя.
    
    Args:
        message (dict): Объект сообщения Telegram
        
    Returns:
        int: chat_id или None, если chat_id отсутствует
    """
    
    chat_id, first_name, last_name, username, date = extract_user_data(message)

    
    if not chat_id:
        return None
        
    UserProfileModel.objects.update_or_create(
        chat_id=chat_id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "date": date,
        },
    )
    
    return chat_id


def send_message(chat_id, text):
    """
    Отправляет сообщение в Telegram.
    
    Args:
        chat_id (int): ID чата Telegram
        text (str): Текст сообщения
        
    Returns:
        dict: Ответ API Telegram или сообщение об ошибке
    """
    telegram_url = settings.TELEGRAM_API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "Открыть веб-апп", "url": f"https://{settings.URL_NGROK}/web_app/{chat_id}"}]
            ]
        },
    }

    try:
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        logger.error(f"Ответ сервера: {response.text if 'response' in locals() else 'Нет ответа'}")
        return {"ok": False, "error": str(e)}


@csrf_exempt
def telegram_webhook(request):
    """
    Webhook для приема обновлений от Telegram бота.
    
    Args:
        request: HTTP запрос Django
        
    Returns:
        JsonResponse: Ответ для Telegram API
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get("message", {})
        
        if not message:
            return JsonResponse({"ok": True})

        text = message.get("text", "")
        
        if text == "/start":
            chat_id = handle_start(message)
            if chat_id:
                response_text = "Привет Мир"
                send_message(chat_id, response_text)
        
        return JsonResponse({"ok": True})
    except Exception as e:
        logger.error(f"Ошибка в обработке webhook: {e}")
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

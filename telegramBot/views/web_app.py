from django.shortcuts import render
from django.views import View
from telegramBot.models import *


class WebApp(View):

    def get(self, request, chat_id):
        """
        Обрабатывает GET-запрос и возвращает страницу с деталями пользователя и списками категорий.

        Args:
            request (HttpRequest): Объект запроса.
            chat_id (int): Уникальный идентификатор чата пользователя, который используется для поиска в базе данных.

        Returns:
            HttpResponse: Ответ с рендерингом страницы webApp.html с контекстом.
        """
        
        context = {
            "user": UserProfileModel.objects.filter(chat_id=chat_id).first(),
            "category": Category.objects.all(),
            "categoryItem": CategoryItem.objects.all(),
        }
        return render(request, "webApp.html", context)
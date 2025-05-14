from django.shortcuts import render
from django.views import View
from telegramBot.models import *


class DetailUserView(View):


    def get(self, request):
        
        """
        Обрабатывает GET-запрос и возвращает страницу с деталями пользователей.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с рендерингом страницы detailUser.html с контекстом.
        """
        
        context = {
            "user": UserProfileModel.objects.all()
        }
        return render(request, "detailUser.html", context)
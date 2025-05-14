from django.db import models


class UserProfileModel(models.Model):
    """
    Модель для хранения информации о пользователях, зарегистрированных в Telegram.
    """

    chat_id = models.BigIntegerField(
        verbose_name="ID чата", unique=True, help_text="ID чата в Телеграмме"
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=255,
        help_text="Имя пользователя в Телеграмме",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=255,
        help_text="Фамилия пользователя в Телеграмме",
        blank=True,
        null=True,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=255,
        help_text="Имя пользователя в Телеграмме",
    )
    date = models.DateTimeField(
        verbose_name="Дата регистрации",
        auto_now_add=True,
        help_text="Дата регистрации пользователя",
    )

    class Meta:
        indexes = [models.Index(fields=["chat_id"])]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

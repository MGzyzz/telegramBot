from django.db import models


class Category(models.Model):
    """
    Модель для хранения типов категорий, например, фруктов, овощей и т.п.
    
    Эта модель используется для организации объектов в разные категории.
    """

    name = models.CharField(
        verbose_name="Название категории",
        max_length=255,
        help_text="Название категории",
    )

    def __str__(self):
        return f"{self.name}"


class CategoryItem(models.Model):
    """
    Модель для хранения типов объектов, которые принадлежат определенной категории.
    
    Включает связь с моделью Category для классификации объектов.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Категория",
        help_text="Категория, к которой принадлежит объект",
    )

    name = models.CharField(
        verbose_name="Название объекта",
        max_length=255,
        help_text="Название объекта",
    )

    def __str__(self):
        return f"{self.category} - {self.name}"

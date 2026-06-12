from django.db import models
from django.contrib.auth.models import User

# 1. Таблица Мероприятий (Концерты, спектакли и т.д.)
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание")
    date = models.DateTimeField(verbose_name="Дата и время проведения")
    venue = models.CharField(max_length=200, verbose_name="Место проведения")

    def __str__(self):
        return self.title

# 2. Таблица Билетов (Категории мест для конкретного мероприятия)
class Ticket(models.Model):
    # Связь "Один ко многим": у одного мероприятия может быть много билетов
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets', verbose_name="Мероприятие")
    ticket_type = models.CharField(max_length=50, verbose_name="Тип билета (VIP, Стандарт, Фан-зона)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Количество доступных мест")

    def __str__(self):
        return f"{self.event.title} - {self.ticket_type} ({self.price} тг.)"

# 3. Таблица Бронирований (Заказы пользователей)
class Booking(models.Model):
    # Связь с пользователем сайта
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    # Связь с конкретным типом билета
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Билет")
    quantity_reserved = models.PositiveIntegerField(default=1, verbose_name="Количество купленных билетов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время заказа")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"
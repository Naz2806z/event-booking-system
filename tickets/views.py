from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Ticket, Booking

# 1. Главная страница со списком всех мероприятий
def event_list(view_request):
    events = Event.objects.all()
    return render(view_request, 'tickets/event_list.html', {'events': events})

# 2. Страница конкретного мероприятия и его билетов
def event_detail(view_request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(view_request, 'tickets/event_detail.html', {'event': event})

# 3. Покупка билета (Доступно только вошедшим пользователям)
@login_required
def buy_ticket(view_request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if view_request.method == 'POST':
        qty = int(view_request.POST.get('quantity', 1))
        if ticket.quantity >= qty:
            ticket.quantity -= qty
            ticket.save()
            Booking.objects.create(user=view_request.user, ticket=ticket, quantity_reserved=qty)
            return redirect('my_bookings')
    return redirect('event_detail', pk=ticket.event.id)
@login_required
def delete_booking(view_request, booking_id):
    # Находим бронирование по его ID, если оно принадлежит текущему пользователю
    booking = get_object_or_404(Booking, id=booking_id, user=view_request.user)
    
    # Возвращаем билеты обратно в «наличие» перед удалением брони
    ticket = booking.ticket
    ticket.quantity += booking.quantity_reserved  # Вот тут исправь на quantity_reserved!
    ticket.save()
    booking.delete()
    
    # Перенаправляем пользователя обратно на страницу его бронирований
    return redirect('my_bookings')

@login_required
def my_bookings(view_request):
    bookings = Booking.objects.filter(user=view_request.user)
    return render(view_request, 'tickets/my_bookings.html', {'bookings': bookings})
from django.shortcuts import render
from django.http import JsonResponse
import random

def about_and_support(request):
    return render(request, 'tickets/about_support.html')

def ai_assistant_api(request):
    """Локальный ИИ-ассистент, работающий без интернета"""
    if request.method == "POST":
        user_message = request.POST.get("message", "").lower().strip()
        
        # База знаний нашего ИИ (работает локально!)
        if "привет" in user_message or "здравствуй" in user_message:
            reply = "Привет! Я твой персональный ИИ-ассистент билетного сервиса. Чем могу помочь?"
        elif "как удалить" in user_message or "отменить" in user_message:
            reply = "Чтобы отменить бронь, перейдите в меню 'Мои бронирования' и нажмите кнопку 'Удалить' напротив нужного билета."
        elif "купить" in user_message or "забронировать" in user_message:
            reply = "Выберите любое мероприятие на главной странице, нажмите 'Подробнее', выберите тип билета и нажмите 'Купить'."
        elif "монеточка" in user_message or "концерт" in user_message:
            reply = "Концерт Монеточки — одно из наших самых популярных событий! Места в Фан-зону еще есть, успейте забронировать."
        elif "поддержка" in user_message or "помощь" in user_message:
            reply = "Служба поддержки работает круглосуточно. Вы можете связаться с автором проекта по почте: support@eventnet.local"
        elif "кто автор" in user_message or "создатель" in user_message:
            reply = "Автор этого замечательного проекта — будущий топовый Fullstack-разработчик! Проект выполнен на базе Django 6.0."
        else:
            # Если ИИ "задумался", выдаем умные общие ответы
            random_replies = [
                "Интересный вопрос! Наш сервис полностью автоматизирован. Попробуйте проверить статус в личном кабинете.",
                "Я обрабатываю ваш запрос... На данный момент все системы бронирования работают в штатном режиме.",
                "Как ваш ИИ-помощник, рекомендую проверить раздел 'Мои бронирования', там доступно управление всеми билетами."
            ]
            reply = random.choice(random_replies)
            from django.shortcuts import redirect, get_object_or_404

def pay_with_kaspi(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Имитируем успешную оплату
    booking.is_paid = True
    booking.save()
    return redirect('my_bookings')
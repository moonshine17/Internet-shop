import smtplib

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings

from carts.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        message = "Ваш заказ:\n" # Начать с байтовой строки
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.total_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                       В наличии - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()
                            message += f"{name} - {quantity} шт\n"  # Добавить строку в байтовый объект
                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()
                        # send_order_confirmation_email(request)
                        send_order_confirmation_email(request, message)
                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'orders': True,
    }
    return render(request, 'orders/create_order.html', context=context)

def send_order_confirmation_email(request, message):
    sender = "udonik0604@mail.ru"
    user_email = request.user.email
    password = ("aeqJfZNkQs9QGWE5dtpx")
    email_message = f"Subject: Вы оформили заказ со следующим содержимым: \n\n{message}".encode("utf-8")
    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, user_email, email_message)

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!",
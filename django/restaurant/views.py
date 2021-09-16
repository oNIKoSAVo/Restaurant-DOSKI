from django.db.models.aggregates import Sum
import requests
from restaurant.lib.payment import Payment
import sys
import json
import random
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.db.models import Q, Count
from django.http.response import JsonResponse
from restaurant.models import Feedback, Franchising, Reservation, Restaraunt, Сareer, Menue, Category, Event, MenuInOrder, Order, Profile
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.py.html', {'data': sys._getframe(0).f_code.co_name})

@require_http_methods(["POST"])
def singup(request):
    phone = request.POST.get('phone') #TODO NEED VALIDATE PHONE NUMBER

    user = User.objects.filter(username=phone)
    if(user.exists()):
        return JsonResponse({"error": "Такой номер уже зарегестрирован"})
    else:
        password = ''.join(
            random.choice('1234567890') for _ in range(4))

        user = User.objects.create_user(username=phone, password=password)
        profile = Profile.objects.create(
            user=user, phone=phone)
        
        if(user and profile):
            return JsonResponse({"success": "Успешно зарегестрирован", "password": password})

    return JsonResponse({"error": "Ошибка..."})

@require_http_methods(["POST"])
def signin(request):
    phone = request.POST.get('phone') #TODO NEED VALIDATE PHONE NUMBER
    password = request.POST.get('password')
    user = authenticate(request, username=phone, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": "Прошел"})
    else:
        return JsonResponse({"error": "НЕПРЕЛ"})


def personal(request):
    if not request.user.is_authenticated:
        return redirect('/#signin')

    user = request.user
    reservations = Reservation.objects.filter(phone=request.user.profile.phone)
    results = []
    for order in user.orders.all():
        results.append({
            "order": order,
            "menue": order.menues
                .values('menue__dish', 'menue__image', 'menue_id')
                .annotate(total=Count('id')).annotate(total_price=Sum('menue__price'))
        })
    return render(request, 'personal.py.html', {'reservations': reservations, 'results': results})


def menu(request):
    categories = Category.get_without(categories_skip=[
        "Сигареты/Кальяны",
        "Сигареты",
        "Богаткова",
        "Гоголя",
        "Калинина",
        "Ленина",
        "Маркса",
        "Фрунзе",
        "Мелкоштучка",
        "Упаковка",
        "Добавки",
        "Соусы",
        "Конфликт-меню",
        "Сиропы",
        "Меню развлечений",
        "Билеты, Вход",
        "Бронь, Аренда",
        "Игры, Развлечения",
        "Спец.предложения",
        "Яндекс Доставка",
        "Доставка"
    ])

    return render(request, 'menu.py.html', {'menues': Menue.objects.all(), 'categories': categories})


def delivery(request):
    categories = Category.get_without(categories_skip=[
        "Сигареты/Кальяны",
        "Сигареты",
        "Богаткова",
        "Гоголя",
        "Калинина",
        "Пиво",
        "Пиво бутылочное",
        "Ленина",
        "Маркса",
        "Фрунзе",
        "Пиво разливное",
        "Мелкоштучка",
        "Упаковка",
        "Пиво в башнях",
        "Кальян",
        "Вино/Вермут/Шампанское",
        "Вино бокалами",
        "Вино бутылками",
        "Вермут",
        "Шампанское",
        "Крепкий алкоголь",
        "Джин",
        "Ликер, Настойка",
        "Абсент",
        "Текила",
        "Коньяк",
        "Виски",
        "Водка",
        "Ром",
        "Алкогольные коктейли",
        "Пати Миксы",
        "Лонги",
        "Шоты",
        "Добавки",
        "Соусы",
        "Конфликт-меню",
        "Сиропы",
        "Меню развлечений",
        "Билеты, Вход",
        "Бронь, Аренда",
        "Игры, Развлечения",
        "Спец.предложения",
        "Яндекс Доставка",
        "Доставка"
    ])

    return render(request, 'delivery.py.html', {'categories': categories})


def reservation(request):
    if request.method == "POST":
        date = request.POST.get('date')
        time_str_start = request.POST.get('start')
        time_str_end = request.POST.get('end')

        date_start = datetime.strptime(
            date + " " + time_str_start, '%d/%m/%Y %H:%M')
        date_end = datetime.strptime(
            date + " " + time_str_end, '%d/%m/%Y %H:%M')
        if request.POST.get('type') == "check":
            reservations = Reservation.objects.filter(end__gte=date_start)
            return JsonResponse({"tables": [reserv.table for reserv in reservations]})
        else:
            reservation = Reservation.objects.create(
                restaraunt=Restaraunt.objects.get(
                    pk=request.POST.get('restaraunt')),
                start=date_start,
                end=date_end,
                persons=request.POST.get('persons'),
                table=request.POST.get('table'),
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                description=request.POST.get('description')
            )
            if(reservation):
                return JsonResponse({"status": "success", "id": reservation.id})
            else:
                return JsonResponse({"status": "error"})
    # if request.GET.get('date') is not None and requests.GET.get('restaraunt') is not None:
    #     restaraunts = Restaraunt.objects.all()
    # else:
    restaraunts = Restaraunt.objects.all()
    restaraunts = [{
        'id': restaraunt.id,
        'text': restaraunt.address,
        'schemes': [{
            'id': schema.id,
            'url': schema.schema.url,
            'description': schema.description
        }for schema in restaraunt.schemes.all()]
    }for restaraunt in restaraunts
    ]
    return render(request, 'reservation.py.html', {'data': sys._getframe(0).f_code.co_name, 'props': {'restaraunts': restaraunts, 'reservation': {'restaraunt_id': request.GET.get('restaraunt'), 'date': request.GET.get('date')}}})


def preorder(request):
    return render(request, 'preorder.py.html', {'menues': Menue.objects.all(), 'categories': Category.objects.all()})


def feedback(request):
    if request.method == "POST":
        feedback = Feedback.objects.create(name=request.POST.get(
            'name'), phone=request.POST.get('phone'), description=request.POST.get('description'))
        if(feedback):
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})
    return render(request, 'feedback.py.html', {'data': sys._getframe(0).f_code.co_name})


def events(request):
    return render(request, 'events.py.html', {'events': Event.objects.all()})


def career(request):
    if request.method == "POST":
        b_day = datetime.strptime(request.POST.get('b_day'), '%d/%m/%Y')
        career = Сareer.objects.create(
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            position=request.POST.get('position'),
            city=request.POST.get('city'),
            bar=request.POST.get('bar'),
            b_day=b_day,
            citizenship=request.POST.get('citizenship'),
            about=request.POST.get('about'),
        )
        if(career):
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})
    return render(request, 'career.py.html', {'data': sys._getframe(0).f_code.co_name})


def franchise(request):
    if request.method == "POST":
        franchise = Franchising.objects.create(name=request.POST.get(
            'name'), phone=request.POST.get('phone'))
        if(franchise):
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})
    return render(request, 'franchise.py.html', {'data': sys._getframe(0).f_code.co_name})


def contacts(request):
    return render(request, 'contacts.py.html', {'data': sys._getframe(0).f_code.co_name})


def create_order(request):
    data = json.loads(request.body)
    menue = data["menue"]
    fio = data["fio"]
    address = data["address"]
    phone = data["phone"]
    comment = data["comment"]
    payment_type = data["paymentType"]

    profile = Profile.objects.filter(phone=phone)
    if(not profile.exists()):
        user = User.objects.create_user(username=phone, password=''.join(
            random.choice('1234567890') for _ in range(4)))
        if(len(fio.split(" ")) >= 3):
            first_name = fio.split(" ")[1]
            second_name = fio.split(" ")[2]
            last_name = fio.split(" ")[0]
        else:
            first_name = fio
            second_name = fio
            last_name = fio

        profile = Profile.objects.create(
            user=user, first_name=first_name, second_name=second_name, last_name=last_name, phone=phone)
    else:
        user = profile.first().user

    menues = []
    receipt = []
    total_price = 0
    for m in menue:
        menue_id = m["id"]
        quantity = m["quantity"]
        menue_item = Menue.objects.get(id=menue_id)
        receipt.append({
            "name": menue_item.dish,
            "price": menue_item.price,
            "discount": 0,
            "resultPrice": 10,
            "quantity": quantity
        })
        for q in range(quantity):
            total_price += menue_item.price
            menues.append(menue_item)
    order = Order.objects.create(user=user, restaraunt_id=1, price=total_price,
                                 payment=payment_type, comment=comment, address=address)

    for m in menues:
        MenuInOrder.objects.create(menue=m, order=order)

    payment = Payment().create_payment(order=order, receipt=receipt)  # payment_url
    # payment = Payment().create_terminal(order=order) # link
    print(payment)
    if("payment_url" in payment):
        return JsonResponse({"payment_url": payment["payment_url"]})
    else:
        return JsonResponse({"error": "can't create payment link"})

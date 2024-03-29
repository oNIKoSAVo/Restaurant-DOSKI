from django.db.models.expressions import F
from restaurant.lib.sms import Sms
from django.db.models.aggregates import Sum
from restaurant.lib.payment import Payment
import sys
import re
import json
import requests
import random
from datetime import datetime
from datetime import timedelta
import xlsxwriter
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .lib.helpers import filter_categories

from django.db.models import Q, Count, Prefetch
from django.http import HttpResponse, HttpResponseNotFound
from django.http.response import JsonResponse
from restaurant.models import (Feedback, Franchising, Promotion, 
                               Reservation, Restaraunt, Career, Menue, 
                               Category, Event, MenuInOrder, Order, 
                               Profile, City, PreOrder, MenuInPreOrder, 
                               MenueInRestaraunt, ReservationStatusType, 
                               Setting, PaymentTypes, TelegramUser)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings as django_settings
from restaurant.management.commands.import_menue import RKEEPER_CATEGORY
from restaurant.util import (generate_response_preorder_pdf, 
                             generate_pdf,
                             notification,
                             telegram_updates,)

from django.core.files.base import ContentFile, File

def index(request):
    setting = Setting.objects.all().last()
    ctx = {
        'promotions': Promotion.objects.order_by('-priority'), 
        'main_banner': setting.main_banner
    }
    return render(request, 'index.py.html', ctx)


def set_city_id(request):
    city_id = request.POST.get('id') if request.POST else request.GET.get('id')
    back_to = request.META.get('HTTP_REFERER') if request.META.get(
        'HTTP_REFERER') else "/"
    try:
        request.session['city'] = City.objects.get(pk=city_id).id
    except City.DoesNotExist:
        pass
    return redirect(back_to)


@require_http_methods(["POST"])
def signup(request):
    phone = request.POST.get('phone')
    cleanphone = re.sub('\W+', '', phone)    

    try:
        user = User.objects.get(username=cleanphone)
        user_exists = True
    except ObjectDoesNotExist:
        user_exists = False

    if user_exists:
        if user.profile.is_deleted:
            password = ''.join(
                random.choice('1234567890') for _ in range(4))

            user.set_password(password)
            user.save()

            prof = user.profile
            prof.is_deleted = False
            prof.save()

            Sms().send(cleanphone, password)

            return JsonResponse({"success": "Аккаунт успешно восстановлен"})

        resp = {
                "error": "Такой номер уже зарегестрирован",
                "error_code": 2
            }
        return JsonResponse(resp)
    else:
        password = ''.join(
            random.choice('1234567890') for _ in range(4))

        user = User.objects.create_user(username=cleanphone, password=password)
        profile = Profile.objects.create(
            user=user, phone=cleanphone)

        Sms().send(cleanphone, password)

        if (user and profile):
            return JsonResponse({"success": "Успешно зарегестрирован"})

    return JsonResponse({"error": "Ошибка..."})


@require_http_methods(["POST"])
def signin(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')

    cleanphone = re.sub('\W+', '', phone)
    user = authenticate(request, username=cleanphone, password=password)
    
    if user.profile.is_deleted:
        return JsonResponse({"error": "Пользователь с таким телефоном был удалён.", 
                            "error_code": 1})
    if user is not None:
        login(request, user)

        if user.is_staff:
            return JsonResponse({"success": "Прошел", 'is_staff': True})
        
        return JsonResponse({"success": "Прошел"})
    else:
        return JsonResponse({"error": "НЕПРЕЛ"})


@require_http_methods(["POST"])
def exit(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"success": "You're free now."})

@require_http_methods(["POST"])
def deactivate(request):
    if request.user.is_authenticated:
        profile = request.user.profile

        if profile:
            profile.is_deleted = True
            profile.save()

        logout(request)

    return JsonResponse({"success": "Прошел"})

@require_http_methods(["POST"])
def recovery(request):
    phone = request.POST.get('phone')
    password = ''.join(
        random.choice('1234567890') for _ in range(4))

    cleanphone = re.sub('\W+', '', phone)

    try:
        user = User.objects.get(username=cleanphone)

        if user.profile.is_deleted:
            return JsonResponse({"error": "Пользователь с таким телефоном был удалён.", 
                                "error_code": 1})
                                
        user.set_password(password)
        user.save()

        Sms().send(cleanphone, password)

        return JsonResponse({"success": "Прошел"})
    except User.DoesNotExist:
        return JsonResponse({"error": "НЕПРЕЛ"})


@require_http_methods(["POST"])
def captcha(request):
    token = request.POST.get('token')
    print(token)
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', headers={
        'Content-type': 'application/x-www-form-urlencoded'},
        data={"secret": "6Ldt-3IdAAAAAIz1DsZ4sBrShbpa5gGA7QcN-3zy", "response": token})
    response_json = json.loads(response.text)
    print(response_json)
    return JsonResponse({"success": response_json['success']})


def personal(request):
    """
    update user data
    """
    if not request.user.is_authenticated:
        print('\n\nUser is not authenticated __\n\n')
        return redirect('/#signin')

    if request.method == "POST":
        data = json.loads(request.body)
        profile = Profile.objects.get(user=request.user)
        fio = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'second_name': data.get('second_name')
        }
        # phone = data.get('phone')
        birthday = data['birthday']
        email = data['email']
        password = data['password']

        print('\n\nUser is authenticated __\n\n')

        if fio:
            if type(fio['last_name']) == str:
                profile.last_name = fio['last_name']
            if type(fio['first_name']) == str:
                profile.first_name = fio['first_name']
            if type(fio['second_name']) == str:
                profile.second_name = fio['second_name']

        # if phone:
        #     request.user.username = profile.phone = re.sub('\W+', '', phone)
        #     request.user.save()

        if birthday:
            profile.birthday = birthday

        if email:
            profile.email = email


        if password:
            user = request.user
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            profile.is_changed_password = True

        profile.save()

        return JsonResponse({"success": "Прошел"})

    user = request.user
    reservations = user.reservations.all()
    results = []
    for order in user.orders.all():
        menue = order.menues\
            .values('menue__dish', 'menue__image', 'menue_id', 'menue__in_restaraunt__price')\
            .annotate(total=Count('id'))\
            .prefetch_related(
                Prefetch('menue__in_restaraunt', 
                    queryset=MenueInRestaraunt
                        .objects.filter(restaraunt=order.restaraunt)
                )
            )\
            .annotate(total_price=F('total') * F('menue__in_restaraunt__price'))

        results.append({
            "order": order,
            "menue": menue
        })
        
    return render(request, 'personal.py.html', {'reservations': reservations, 'results': results})


def menu(request):
    categories = Category.get_without(categories_skip=[
        RKEEPER_CATEGORY,
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

    categories = categories.annotate(menue_count=Count(
        'menues__id')).filter(menue_count__gt=0).order_by('name')
        # .filter(menues__in_restaraunt__menue__category__in=categories)

    city = City.objects.get(pk=request.session.get('city', 1))
    restaraunt = Restaraunt.objects.filter(city=city).first()

    # for category in categories:
    #     setattr(category, 'menues_in_rastaraunt',
    #             MenueInRestaraunt.objects.filter(menue__category=category, restaraunt=restaraunt))
    #     filtered_dishes = []
    #     for dish in category.menues_in_rastaraunt:
    #         if not dish.price == 9.223372036854776e+16:
    #             filtered_dishes.append(dish)
    #     category.menues_in_rastaraunt = filtered_dishes
    #     print('category', category.__dict__)
    return render(request, 'menu.py.html', {
        'categories': filter_categories(categories, restaraunt),
        'menue_file': restaraunt.menue_file.url if restaraunt.menue_file else "#"
    })


def delivery(request):
    categories = Category.get_without(categories_skip=[
        RKEEPER_CATEGORY,
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

    categories = categories.annotate(menue_count=Count('menues__id')) \
        .filter(menue_count__gt=0).order_by('name')

    session_rest = request.session.get('restaraunt', 1)

    if session_rest:
        restaraunt = Restaraunt.objects.get(pk=request.session.get('restaraunt', 1))
    else:
        city = City.objects.get(pk=request.session.get('city', 1))
        restaraunt = Restaraunt.objects.filter(city=city).first()

    for category in categories:
        setattr(category, 'menues_in_rastaraunt',
                MenueInRestaraunt.objects.filter(menue__category=category, restaraunt=restaraunt))
    return render(request, 'delivery.py.html', {'categories': filter_categories(categories, restaraunt)})


def set_restaraunt_id(request):
    restaraunt_id = request.POST.get('id') if request.POST else request.GET.get('id')
    back_to = request.META.get('HTTP_REFERER') if request.META.get(
        'HTTP_REFERER') else "/"
    try:
        request.session['restaraunt'] = Restaraunt.objects.get(pk=restaraunt_id).id
    except Restaraunt.DoesNotExist:
        pass
    return redirect(back_to)


def reservation(request):
    #from django.utils import timezone
    if request.method == "POST":
        date = request.POST.get('date')
        time_str_start = request.POST.get('time')
        # time_str_end = request.POST.get('end')

        date_start = datetime.strptime(
            date + " " + time_str_start, '%d/%m/%Y %H:%M')

        time_start = datetime.strptime(time_str_start, '%H:%M').time()
        # date_end = datetime.strptime(
        #     date + " " + time_str_end, '%d/%m/%Y %H:%M')

        # date_start = timezone.make_aware(date_start, timezone.get_default_timezone())

        if request.POST.get('type') == "check":
            today_start = date_start.replace(hour=0, minute=0, second=0)
            today_end = date_start.replace(hour=23, minute=59, second=59)

            reservations = Reservation.objects.filter(
                restaraunt=request.POST.get('restaraunt'), 
                start__lte=today_end, start__gte=today_start
            )\
                .filter(Q(status=ReservationStatusType.APPROVED) | Q(status=ReservationStatusType.WAIT))

            return JsonResponse({"tables": [reserv.table for reserv in reservations]})
        else:
            setting = Setting.objects.all().last()
            if setting.allow_period_reservation:
                check_date = datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=setting.allow_period_reservation)
                if check_date < date_start:
                    return JsonResponse({"status": "error", "message": f"Период бронирования не может превышать {setting.allow_period_reservation} дней"})

            if setting.allow_time_reservation_start and setting.allow_time_reservation_end:
                if not setting.allow_time_reservation_start <= time_start <= setting.allow_time_reservation_end:
                    return JsonResponse({"status": "error", "message": f"Бронирование доступно с {setting.allow_time_reservation_start} по {setting.allow_time_reservation_end}"})

            if date_start < datetime.now():
                return JsonResponse({"status": "error", "message": "Бронирование за прошедшее время"})

            cleanphone = re.sub('\W+', '', request.POST.get('phone'))
            profile = Profile.objects.filter(phone=cleanphone)
            reservation_name = request.POST.get('name')
            if (not profile.exists()):
                password = ''.join(
                    random.choice('1234567890') for _ in range(4))
                user = User.objects.create_user(
                    username=cleanphone, password=password)
                profile = Profile.objects.create(
                    user=user, first_name=reservation_name, phone=cleanphone)

                Sms().send(cleanphone, password)
            else:
                profile = profile.first()
                user = profile.user


            num_persons = request.POST.get('persons')
            table_id = request.POST.get('table')
            userphone = request.POST.get('phone')
            restaraunt = Restaraunt.objects.get(pk=request.POST.get('restaraunt'))

            reservation = Reservation.objects.create(
                user=user,
                restaraunt=restaraunt,
                start=date_start,
                end=date_start,  # hack
                persons=num_persons,
                table=table_id,
                name=reservation_name,
                phone=userphone,
                description=request.POST.get('description')
            )

            if (reservation):
                request.session['reservation'] = reservation.id
                request.session['restaraunt'] = request.POST.get('restaraunt')

                updates = telegram_updates()

                if updates:
                    updates_list = updates['result']
                    if len(updates_list):
                        chat = updates_list[0]['message']['chat']
                        print(chat)
                        teleuser = TelegramUser.objects.filter(username=chat['username']).first()
                        if teleuser:
                            teleuser.chat_id = chat['id']
                            teleuser.save()

                msg = \
                    f'{reservation_name} забронировал(а) стол {table_id} ' \
                    f'в {date_start} на {num_persons} человек(а). ' \
                    f'Номер: {userphone}. Ресторан на улице {restaraunt.address}'

                gr = Group.objects.filter(name='бронирование').first()
                if gr:
                    teleusers = TelegramUser.objects.filter(user__groups=gr) \
                        .filter(user__groups=restaraunt.group)
                    
                    for teleuser in teleusers:
                        notification(teleuser.chat_id, message=msg)
                
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
        'tables': [{
            'photo': photo_table.table.url,
            'description': photo_table.description,
            'table': photo_table.table_number
        } for photo_table in restaraunt.tables.all()],
        'schemes': [{
            'id': schema.id,
            'url': schema.schema.url,
            'description': schema.description
        } for schema in restaraunt.schemes.all()]
    } for restaraunt in restaraunts
    ]
    return render(request, 'reservation.py.html', {'data': sys._getframe(0).f_code.co_name,
                                                   'props': {'restaraunts': restaraunts, 'reservation': {
                                                       'restaraunt_id': request.GET.get('restaraunt'),
                                                       'date': request.GET.get('date')}}})


def preorder(request):
    # request data
    # {
    #     "restaraunt": 1,
    #     "comment": "about",
    #     "reservation": 1,
    #     "menue": [
    #         {
    #             "id": "416",
    #             "quantity": 2
    #         }
    #     ]
    # }
    if request.method == "POST":
        data = json.loads(request.body)
        city = City.objects.get(pk=request.session.get('city', 1))
        restaraunt = Restaraunt.objects.filter(city=city).first().id
        if request.session.get('restaraunt',  None) is not None:
            restaraunt = request.session.get('restaraunt',  None)

        comment = data['comment']
        menue = data["menue"]
        reservation = request.session.get('reservation', '')
        menues = []
        total_price = 0
        for m in menue:
            menue_id = m["id"]
            quantity = m["quantity"]
            menue_item = Menue.objects.get(id=menue_id)
            menue_in_restaraunt = MenueInRestaraunt.objects.filter(
                menue=menue_item, restaraunt=restaraunt).first()
            for q in range(quantity):
                total_price += menue_in_restaraunt.price
                menues.append(menue_item)
        preorder = PreOrder.objects.create(restaraunt_id=restaraunt, price=total_price,
                                           comment=comment, reservation_id=reservation)

        for m in menues:
            MenuInPreOrder.objects.create(menue=m, preorder=preorder)

        pdfbytes = generate_pdf(preorder)

        import os, io
        with io.BytesIO() as fi:
            fi.write(pdfbytes)
            print('-'*30+'\n', f'{preorder.id}.pdf\n', '-'*30, sep='')
            preorder.filepdf = File(fi, name=f'{preorder.id}.pdf')
            preorder.save()

        return JsonResponse({"status": "success", "id": preorder.id, "filepdf": preorder.filepdf.url})

    categories = Category.get_without(categories_skip=[
        RKEEPER_CATEGORY,
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

    categories = categories.annotate(menue_count=Count(
        'menues__id')).filter(menue_count__gt=0).order_by('name')
    city = City.objects.get(pk=request.session.get('city', 1))
    restaraunt = Restaraunt.objects.filter(city=city).first()
    # for category in categories:
    #     setattr(category, 'menues_in_rastaraunt',
    #             MenueInRestaraunt.objects.filter(menue__category=category, restaraunt=restaraunt))
    if "restaraunt" in request.session:
        del request.session["restaraunt"]

    if "reservation" in request.session:
        del request.session["reservation"]

    return render(request, 'preorder.py.html', {'categories': filter_categories(categories, restaraunt)})


def download_preorder(request):
    id = request.GET.get('id')
    try:
        preorder = PreOrder.objects.get(pk=id)
        return generate_response_preorder_pdf(preorder=preorder)
    except PreOrder.DoesNotExist:
        return HttpResponseNotFound('Page not found')

# def download_preorder(request):
#     id = request.GET.get('id')
#     try:
#         preorder = PreOrder.objects.get(pk=id)
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="preorder.xlsx"'

#         workbook = xlsxwriter.Workbook(response, {'in_memory': True})
#         worksheet = workbook.add_worksheet()
#         row = 0
#         col = 0
#         # worksheet.write(row, col, "Предзаказ")
#         for menuinpreorder in preorder.menues.all():
#             menue_in_restaraunt = MenueInRestaraunt.objects.filter(menue=menuinpreorder.menue,
#                                                                    restaraunt=menuinpreorder.preorder.restaraunt).first()
#             worksheet.write(row, col, menuinpreorder.menue.dish)
#             worksheet.write(row, (col + 1), menue_in_restaraunt.price)
#             row += 1

#         worksheet.write(row, col, "Сумма предзаказа")
#         worksheet.write(row, (col + 1), preorder.price)

#         workbook.close()
#         return response
#     except PreOrder.DoesNotExist:
#         return HttpResponseNotFound('Page not found')


def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        feedback = Feedback.objects.create(name=name, phone=phone, description=description)

        if (feedback):
            settings = Setting.objects.first()
            # f'phone: {phone}\nname: {name}'
            email_body = f"Имя: {name}\n" \
                         f"Телефон: {phone}\n" \
                         f"Описание: {description}"

            send_mail(
                'respublica:Отзыв', 
                email_body,
                django_settings.EMAIL_HOST_USER, 
                [settings.career_email])

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})
    return render(request, 'feedback.py.html', {'data': sys._getframe(0).f_code.co_name})


def events(request):
    city_id = request.session.get('city')
    city = City.objects.filter(id=city_id).first()

    if city:
        events = Event.objects.filter(city=city, date__gt=datetime.now())
    else: 
        events = Event.objects.filter(date__gt=datetime.now())

    return render(request, 'events.py.html', {'events': events})


def career(request):
    if request.method == "POST":
        b_day = datetime.strptime(request.POST.get('b_day'), '%d/%m/%Y')
        first_name = request.POST.get('first_name'),
        middle_name = request.POST.get('middle_name'),
        last_name = request.POST.get('last_name'),
        phone = request.POST.get('phone'),
        position = request.POST.get('position'),
        city = request.POST.get('city'),
        bar = request.POST.get('bar'),
        citizenship = request.POST.get('citizenship'),
        about = request.POST.get('about'),

        career = Career.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
            position=position,
            city=city,
            bar=bar,
            b_day=b_day,
            citizenship=citizenship,
            about=about,
        )

        if (career):
            settings = Setting.objects.first()
            # f'phone: {phone}\nname: {name}'
            email_body = f"Имя: {first_name} {middle_name} {last_name}\n" \
                         f"Телефон: {phone}\n" \
                         f"Позиция: {position}\n" \
                         f"Город: {city}\n" \
                         f"Бар: {bar}\n" \
                         f"Дата рождения: {b_day}\n" \
                         f"Гражданство: {citizenship}\n" \
                         f"Обо мне: {about}\n --- \nbay bay!"

            send_mail(
                'respublica:Заявка на карьеру', 
                email_body,
                django_settings.EMAIL_HOST_USER, 
                [settings.feedback_email])

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})

    settings = Setting.objects.first()
    context = {
        'data': sys._getframe(0).f_code.co_name, 
        'settings': settings
    }
    return render(request, 'career.py.html', context)


def franchise(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        franchise = Franchising.objects.create(name=name, phone=phone)

        if (franchise):
            settings = Setting.objects.first()

            send_mail(
                'respublica:Заявка на франшизу', 
                f'Телефон: {phone}\nИмя: {name}',
                django_settings.EMAIL_HOST_USER, 
                [settings.franchising_email])

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"})
    return render(request, 'franchise.py.html', {'data': sys._getframe(0).f_code.co_name})


def contacts(request):
    return render(request, 'contacts.py.html', {'data': sys._getframe(0).f_code.co_name})

def pclogin(request):
    return render(request, 'pclogin.py.html')

def pcdelivery(request):
    return render(request, 'pcdelivery.py.html')

def pcbooking(request):
    return render(request, 'pcbooking.py.html')

def cabinet(request):
    reservations = Reservation.objects.all()
    orders = Order.objects.all()
    return render(request, 'cabinet.py.html', {'reservations': reservations, 'orders': orders})


def create_order(request):
    data = json.loads(request.body)
    menue = data["menue"]
    fio = data["fio"]
    address = data["address"]
    phone = data["phone"]
    comment = data["comment"]
    payment_type = data["paymentType"]
    print('TEST CREATE ORDER: \n', data)

    cleanphone = re.sub('\W+', '', phone)
    profile = Profile.objects.filter(phone=cleanphone)
    if (not profile.exists()):
        print('CREATING PROFILE')
        password = ''.join(
            random.choice('1234567890') for _ in range(4))
        user = User.objects.create_user(username=cleanphone, password=password)
        if (len(fio.split(" ")) >= 3):
            first_name = fio.split(" ")[1]
            second_name = fio.split(" ")[2]
            last_name = fio.split(" ")[0]
        else:
            first_name = fio
            second_name = fio
            last_name = fio

        profile = Profile.objects.create(
            user=user, first_name=first_name, second_name=second_name, last_name=last_name, phone=cleanphone)

        try:
            Sms().send(cleanphone, password)
        except Exception as ex:
            print(ex)
        
        print('PROFILE CREATED')
    else:
        profile = profile.first()
        user = profile.user

    menues = []
    receipt = []

    total_price = 0
    city = City.objects.get(pk=request.session.get('city', 1))
    restaraunt = Restaraunt.objects.filter(city=city).first()
    print('SESSION CITY', city, restaraunt)

    for m in menue:
        menue_id = m["id"]
        quantity = m["quantity"]
        menue_item = Menue.objects.get(id=menue_id)
        menue_in_restaraunt = MenueInRestaraunt.objects.filter(
            menue=menue_item, restaraunt=restaraunt).first()
        receipt.append({
            "name": menue_item.dish,
            "price": menue_in_restaraunt.price,
            "discount": 0,
            "resultPrice": 10,
            "quantity": quantity
        })
        for q in range(quantity):
            total_price += menue_in_restaraunt.price
            menues.append(menue_item)
    order = Order.objects.create(user=user, restaraunt_id=restaraunt.id, price=total_price,
                                 payment=payment_type, comment=comment, address=address)

    updates = telegram_updates()

    if updates:
        updates_list = updates['result']
        if len(updates_list):
            chat = updates_list[0]['message']['chat']
            print(chat)
            teleuser = TelegramUser.objects.filter(username=chat['username']).first()
            if teleuser:
                teleuser.chat_id = chat['id']
                teleuser.save()

    msg = \
        f'{profile.first_name} сделал заказ по адресу {order.address} ' \
        f'в {order.created_at} на сумму {order.price} р. ' \
        f'Номер: {profile.phone}. Ресторан на улице {restaraunt.address}'

    gr = Group.objects.filter(name='доставка').first()
    if gr:
        teleusers = TelegramUser.objects.filter(user__groups=gr) \
            .filter(user__groups=restaraunt.group)

        for teleuser in teleusers:
            notification(teleuser.chat_id, message=msg)

    for m in menues:
        MenuInOrder.objects.create(menue=m, order=order)
    
    if not (payment_type == PaymentTypes.ONLINE):
        return JsonResponse({"status_code": 401, "message": "Created a new order"})
        
    payment = Payment().create_payment(
        order=order, 
        receipt=receipt, 
        key=restaraunt.payment_key, 
        terminal=restaraunt.payment_terminal_id
    )
    
    # payment_url
    # payment = Payment().create_terminal(order=order) # link
    print('PAYMENT: ', payment)
    if ("payment_url" in payment):
        return JsonResponse({"payment_url": payment["payment_url"]})
    else:
        return JsonResponse({"error": "can't create payment link"})


def restaraunts(request):
    id = request.GET.get('id')
    city = request.GET.get('city')
    if (id):
        restaraunt = Restaraunt.objects.get(pk=id)
        return JsonResponse({
            "address": restaraunt.address,
            "phone": restaraunt.phone,
            "coordinates": restaraunt.coordinates,
            "yandex_eda": restaraunt.yandex_eda,
            "tables": [{
                'table': photo_table.table_number,
                'photo': photo_table.table.url,
                'description': photo_table.description
            } for photo_table in restaraunt.tables.all()],
            "city": {
                "id": restaraunt.city.id,
                "name": restaraunt.city.name,
                "phone": restaraunt.city.phone,
                "instagram": restaraunt.city.instagram,
                "city_timezone": str(restaraunt.city.city_timezone),
                "vk": restaraunt.city.vk,
            },
            "schemes": [{
                "id": schema.id,
                "url": schema.schema.url,
                "description": schema.description
            } for schema in restaraunt.schemes.all()]
        }, safe=False)
    elif (city):
        city = City.objects.get(pk=city)
        restaraunts = city.restaraunts.all()
        response = []
        for restaraunt in restaraunts:
            response.append({
                "id": restaraunt.id,
                "address": restaraunt.address,
                "phone": restaraunt.phone,
                "coordinates": restaraunt.coordinates,
                "yandex_eda": restaraunt.yandex_eda,
                "tables": [{
                    'table': photo_table.table_number,
                    'photo': photo_table.table.url,
                    'description': photo_table.description
                } for photo_table in restaraunt.tables.all()],
                "city": {
                    "id": restaraunt.city.id,
                    "name": restaraunt.city.name,
                    "phone": restaraunt.city.phone,
                    "instagram": restaraunt.city.instagram,
                    "city_timezone": str(restaraunt.city.city_timezone),
                    "vk": restaraunt.city.vk,
                },
                "schemes": [{
                    "id": schema.id,
                    "url": schema.schema.url,
                    "description": schema.description
                } for schema in restaraunt.schemes.all()]
            })
        return JsonResponse(response, safe=False)
    else:
        restaraunts = Restaraunt.objects.all()
        response = []
        for restaraunt in restaraunts:
            response.append({
                "id": restaraunt.id,
                "address": restaraunt.address,
                "phone": restaraunt.phone,
                "coordinates": restaraunt.coordinates,
                "yandex_eda": restaraunt.yandex_eda,
                "tables": [{
                    'table': photo_table.table_number,
                    'photo': photo_table.table.url,
                    'description': photo_table.description
                } for photo_table in restaraunt.tables.all()],
                "city": {
                    "id": restaraunt.city.id,
                    "name": restaraunt.city.name,
                    "phone": restaraunt.city.phone,
                    "instagram": restaraunt.city.instagram,
                    "city_timezone": str(restaraunt.city.city_timezone),
                    "vk": restaraunt.city.vk,
                },
                "schemes": [{
                    "id": schema.id,
                    "url": schema.schema.url,
                    "description": schema.description
                } for schema in restaraunt.schemes.all()]
            })
        return JsonResponse(response, safe=False)


def payment_success(request):
    print(request)
    return JsonResponse({"ok": ".........."})


def payment_fail(request):
    print(request)
    return JsonResponse({"ok": ".........."})

def manager_settings(request):
    setting = Setting.objects.all().last()
    setting.__dict__.pop('_state')
    return JsonResponse({"settings": setting.__dict__})

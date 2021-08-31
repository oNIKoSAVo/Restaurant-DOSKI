import sys
from datetime import datetime

from django.http.response import JsonResponse
from restaurant.models import Feedback, Franchising, Reservation, Restaraunt, Сareer, Menue, Category
from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    return render(request, 'index.py.html', {'data': sys._getframe(0).f_code.co_name})


def menu(request):
    return render(request, 'menu.py.html', {'menues': Menue.objects.all(), 'categories': Category.objects.all() })


def delivery(request):
    return render(request, 'delivery.py.html', {'menues': Menue.objects.all(), 'categories': Category.objects.all()})


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
            return JsonResponse({"tables":[reserv.table for reserv in reservations]})
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
    return render(request, 'reservation.py.html', {'data': sys._getframe(0).f_code.co_name, 'props': {'restaraunts': restaraunts}})


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
    return render(request, 'events.py.html', {'data': sys._getframe(0).f_code.co_name})


def career(request):
    if request.method == "POST":
        career = Сareer.objects.create(
            first_name=request.POST.get('first_name'),
            middle_name=request.POST.get('middle_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            position=request.POST.get('position'),
            city=request.POST.get('city'),
            bar=request.POST.get('bar'),
            b_day=request.POST.get('b_day'),
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


def login(request):
    return render(request, 'login.py.html', {'data': sys._getframe(0).f_code.co_name})

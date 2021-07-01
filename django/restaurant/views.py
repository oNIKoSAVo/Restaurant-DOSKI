from django.http.response import JsonResponse
from restaurant.models import Feedback, Franchising
import sys
from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    return render(request, 'index.py.html', {'data': sys._getframe(0).f_code.co_name})


def menu(request):
    return render(request, 'menu.py.html', {'data': sys._getframe(0).f_code.co_name})


def delivery(request):
    return render(request, 'delivery.py.html', {'data': sys._getframe(0).f_code.co_name})


def reservation(request):
    return render(request, 'reservation.py.html', {'data': sys._getframe(0).f_code.co_name})


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


def job(request):
    return render(request, 'job.py.html', {'data': sys._getframe(0).f_code.co_name})


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

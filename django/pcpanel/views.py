from datetime import datetime, time, timedelta
from django.contrib import messages
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import AccessMixin
from restaurant.models import Order, Reservation, Restaraunt, ReservationStatusType, OrderStatusType

# Create your views here.


class OnlyStuffUserAccessMixin(AccessMixin):
    """Verify that the current user is authenticated and is_stuff."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LoginView(OnlyStuffUserAccessMixin, View):

    def get(self, request):
        today_start = datetime.now().replace(hour=0, minute=0, second=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59)

        if(request.user.is_superuser):
            queryset_reservations = Reservation.objects.filter()
            queryset_order = Order.objects.filter()
        else:
            queryset_reservations = Reservation.objects.filter(
                restaraunt__city__groups__in=request.user.groups.all())
            queryset_order = Order.objects.filter(
                restaraunt__city__groups__in=request.user.groups.all())

        count_new_reservations = queryset_reservations.filter(
            status=ReservationStatusType.WAIT).filter(start__lte=today_end, start__gte=today_start).count()
        count_new_orders = queryset_order.filter(
            status=OrderStatusType.WAIT).filter(created_at__lte=today_end, created_at__gte=today_start).count()

        return render(request, 'pclogin.py.html', {'count_new_reservations': count_new_reservations, 'count_new_orders': count_new_orders})


class BookingView(OnlyStuffUserAccessMixin, View):
    login_url = '/#login'
    redirect_field_name = ''

    def get(self, request):
        today_start = datetime.now().replace(hour=0, minute=0, second=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59)

        if request.user.is_superuser:
            reservarions = Reservation.objects.all()
            filter_restaraunt = Restaraunt.objects.all()
            reservations_processed = Reservation.objects.filter(
                status=ReservationStatusType.APPROVED)
        else:
            reservarions = Reservation.objects.filter(
                restaraunt__city__groups__in=request.user.groups.all())
            filter_restaraunt = Restaraunt.objects.filter(
                city__groups__in=request.user.groups.all())
            reservations_processed = Reservation.objects.filter(
                status=ReservationStatusType.APPROVED).filter(
                restaraunt__city__groups__in=request.user.groups.all())

        reservarions = reservarions.filter(status=ReservationStatusType.WAIT)
        if(request.GET.get('id')):
            try:
                response = reservarions.get(pk=request.GET.get('id'))
                return JsonResponse(model_to_dict(response), safe=False)
            except Reservation.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Reservation not found'}, status=404)

        if(request.GET.get('filter_restaraunt')):
            reservarions = reservarions.filter(
                restaraunt__id=request.GET.get('filter_restaraunt'))
            reservations_processed = reservations_processed.filter(
                restaraunt__id=request.GET.get('filter_restaraunt'))

        if(request.GET.get('filter_date')):
            today_start = datetime.strptime(
                request.GET.get('filter_date'), '%d-%m-%Y').replace(hour=0, minute=0, second=0)
            today_end = datetime.strptime(
                request.GET.get('filter_date'), '%d-%m-%Y').replace(hour=23, minute=59, second=59)

        reservations_processed = reservations_processed.filter(
            start__lte=today_end, start__gte=today_start)
        reservations = reservarions.filter(
            start__lte=today_end, start__gte=today_start)

        return render(request, 'pcbooking.py.html',  {
            'reservations': reservations,
            'reservations_processed': reservations_processed,
            'ReservationStatusType': ReservationStatusType,
            'filter_restaraunt': filter_restaraunt
        })

    def post(self, request):
        id = request.POST.get('id')
        if id:
            params = {key: request.POST.get(key)
                      for key in request.POST.keys()}
            if request.POST.get('date') and request.POST.get('time'):
                date_start = datetime.strptime(
                    params['date'] + " " + params['time'], '%d/%m/%Y %H:%M')

                params['start'] = date_start
                params['end'] = date_start
                del params['date']
                del params['time']

            count = Reservation.objects.filter(pk=id).update(**params)
            if(count > 0):
                messages.success(request, 'Бронирование изменено.')
        return redirect(request.META.get('HTTP_REFERER'))


class DeliveryView(OnlyStuffUserAccessMixin, View):
    login_url = '/#login'
    redirect_field_name = ''

    def get(self, request):
        if request.user.is_superuser:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(
                restaraunt__city__groups__in=request.user.groups.all())

        if(request.GET.get('id')):
            try:
                response = queryset.get(pk=request.GET.get('id'))
                return JsonResponse(model_to_dict(response), safe=False)
            except Order.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

        orders = queryset.filter(status=OrderStatusType.WAIT)
        return render(request, 'pcdelivery.py.html', {'orders': orders, 'OrderStatusType': OrderStatusType})

    def post(self, request):
        id = request.POST.get('id')
        if id:
            params = {key: request.POST.get(key)
                      for key in request.POST.keys()}
            count = Order.objects.filter(pk=id).update(**params)
            if(count > 0):
                messages.success(request, 'Доставка изменена.')
        return redirect(reverse('pcdelivery'))

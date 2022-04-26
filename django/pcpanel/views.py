from datetime import datetime, time, timedelta
from django.contrib import messages
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from restaurant.models import Order, Reservation,\
     Restaraunt, ReservationStatusType, OrderStatusType, Profile

from django.contrib.auth.models import User
import re, random
from restaurant.lib.sms import Sms
from restaurant.models import ReservationStatusType
# Create your views here.


class OnlyStuffUserAccessMixin(AccessMixin):
    """Verify that the current user is authenticated and is_stuff."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LoginView(OnlyStuffUserAccessMixin, View):
    login_url = '/#login'
    redirect_field_name = ''

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

        return render(request, 'pclogin.py.html', {'count_new_reservations': count_new_reservations, 'count_new_orders': count_new_orders, 'pcpanel_main_page': True})


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

            reservation_qs = Reservation.objects.filter(pk=id)
            if params['status'] == str(ReservationStatusType.REJECT):
                cleanphone = re.sub('\W+', '', reservation_qs.first().phone)
                Sms().send(cleanphone, "Ваша бронь была удалена менеджером")

            count = reservation_qs.update(**params)
            if(count > 0):
                messages.success(request, 'Бронирование изменено.')
        else:
            date = request.POST.get('date')
            time_start = request.POST.get('time')
            num_persons = request.POST.get('persons')
            table_id = request.POST.get('table')
            restaraunt_id = request.POST.get('restaraunt')
            restaraunt = Restaraunt.objects.get(pk=restaraunt_id)
            userphone = request.POST.get('phone')
            reservation_name = request.POST.get('name')

            date_start = datetime.strptime(f'{date} {time_start}', '%d/%m/%Y %H:%M')

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
                user = profile.first().user


            Reservation.objects.create(
                user=user,
                restaraunt=restaraunt,
                start=date_start,
                end=date_start, # hack
                persons=num_persons,
                table=table_id,
                name=reservation_name,
                phone=userphone,
                description=request.POST.get('description', ''),
                status=ReservationStatusType.APPROVED
            )

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

        orders = queryset.filter(Q(status=OrderStatusType.WAIT) | 
                                 Q(status=OrderStatusType.APPROVED))

        if(request.GET.get('filter_date')):
            today_start = datetime.strptime(
                request.GET.get('filter_date'), '%d-%m-%Y').replace(hour=0, minute=0, second=0)
            today_end = datetime.strptime(
                request.GET.get('filter_date'), '%d-%m-%Y').replace(hour=23, minute=59, second=59)
            orders = orders.filter(
                created_at__lte=today_end, created_at__gte=today_start)

        orders.order_by('status', '-created_at')

        dishes_of_all_orders = dict()

        for order in orders:
            dishes = {}

            for menue in order.menues.all():
                dish_name = menue.menue.dish
                if dish_name in dishes.keys():
                    dishes[dish_name]['sum_price'] += menue.menue.in_restaraunt.first().price
                    dishes[dish_name]['count'] += 1
                    # dishes[dish_name]['weight'] += int(menue.menue.weight)
                else:
                    dishes[dish_name] = {
                        "order": order,
                        "sum_price": menue.menue.in_restaraunt.first().price,
                        "count": 1,
                        "weight": menue.menue.weight,
                        "image_url": menue.menue.image.url,
                        "name": dish_name,
                    }

            dishes_of_all_orders[order.id] = dishes.values()

        context = {
            'orders': orders, 
            'OrderStatusType': OrderStatusType,
            'dishes_of_all_orders': dishes_of_all_orders
        }
        return render(request, 'pcdelivery.py.html', context)

    def post(self, request):
        id = request.POST.get('id')
        if id:
            params = {key: request.POST.get(key)
                      for key in request.POST.keys()}
            count = Order.objects.filter(pk=id).update(**params)
            if(count > 0):
                messages.success(request, 'Доставка изменена.')
        return redirect(reverse('pcdelivery'))

from django.contrib.auth import models
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.core.management import call_command
from .models import (Category, Feedback, Franchising, 
                     MenuInOrder, Menue, MenueInRestaraunt, 
                     Order, PhotoTable, Profile, Promotion, 
                     Reservation, Restaraunt, Setting, Career, 
                     RestarauntSchema, Event, City, 
                     MenuInPreOrder, PreOrder, TelegramUser)

admin.site.site_header = 'Respublica administrator'

class MenueInRestarauntInLine(admin.TabularInline):
    model = MenueInRestaraunt
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class MenueAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list_object_tools_with_addition_buttons.html"
    
    list_display = ['id', 'image_preview', 'dish', 'category', 'is_active']
    list_filter = ['category',]
    inlines = [MenueInRestarauntInLine]

    def image_preview(self, obj):
        return mark_safe("<img src='/media/{}'  width='100' />".format(obj.image))
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True

    def get_urls(self):
        urls = super(MenueAdmin, self).get_urls()
        custom_urls = [
            url('^run_import/$', self.run_import, name='run_import'),]
        return custom_urls + urls

    def run_import(self, request):
        data = call_command('import_menue')
        self.message_user(request, "Запущен импорт")
        return HttpResponseRedirect("../")
admin.site.register(Menue, MenueAdmin)

class RestarauntSchemaAdmin(admin.StackedInline):
    model = RestarauntSchema

class PhotoTablesAdmin(admin.StackedInline):
    model = PhotoTable

class RestarauntAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone', 'city']
    exclude = ('active_ident',)
    inlines = [RestarauntSchemaAdmin, PhotoTablesAdmin]
admin.site.register(Restaraunt, RestarauntAdmin)
admin.site.register(City)


class MenuInOrderInLine(admin.TabularInline):
    model = MenuInOrder
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaraunt', 'price', 'address', 'created_at',]
    list_filter =['restaraunt', 'price',  'created_at',]
    inlines = [MenuInOrderInLine]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Проверка, является ли пользователь администратором
        if request.user.is_superuser:
            return qs  # Если пользователь является администратором, отображаем все рестораны
        
        # Фильтрация резерваций только для ресторанов, связанных с группой ресторана и группами пользователя
        return qs.filter(restaraunt__group__in=request.user.groups.all())


class MenuInPreOrderInLine(admin.TabularInline):
    model = MenuInPreOrder
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaraunt', 'price', 'created_at',]
    list_filter =['restaraunt', 'price',  'created_at',]
    inlines = [MenuInPreOrderInLine]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Проверка, является ли пользователь администратором
        if request.user.is_superuser:
            return qs  # Если пользователь является администратором, отображаем все рестораны
        
        # Фильтрация резерваций только для ресторанов, связанных с группой ресторана и группами пользователя
        return qs.filter(restaraunt__group__in=request.user.groups.all())


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaraunt', 'persons', 'table', 'start', 'end', 'name', 'phone']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Проверка, является ли пользователь администратором
        if request.user.is_superuser:
            return qs  # Если пользователь является администратором, отображаем все рестораны
        
        # Фильтрация резерваций только для ресторанов, связанных с группой ресторана и группами пользователя
        return qs.filter(restaraunt__group__in=request.user.groups.all())

class CareerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'position']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaraunt', 'date', 'city']

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'description', 'priority']

    def image_preview(self, obj):
        return mark_safe("<img src='/media/{}'  width='100' />".format(obj.image))
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True

class FranchisingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']

admin.site.register(Order, OrderAdmin)
admin.site.register(PreOrder, PreOrderAdmin)

admin.site.register(Profile)
admin.site.register(Category)

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Franchising, FranchisingAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(Reservation, ReservationAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(Promotion, PromotionAdmin)

admin.site.register(Setting)
admin.site.register(TelegramUser)

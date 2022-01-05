from django.contrib.auth import models
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Category, Feedback, Franchising, MenuInOrder, Menue, MenueInRestaraunt, Order, PhotoTable, Profile, Promotion, Reservation, Restaraunt, Setting, Сareer, RestarauntSchema, Event, City, MenuInPreOrder, PreOrder

admin.site.site_header = 'Bardoski administrator'

class MenueInRestarauntInLine(admin.TabularInline):
    model = MenueInRestaraunt
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class MenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'dish', 'category']
    list_filter = ['category',]
    inlines = [MenueInRestarauntInLine]

    def image_preview(self, obj):
        return mark_safe("<img src='/media/{}'  width='100' />".format(obj.image))
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True
admin.site.register(Menue, MenueAdmin)

class RestarauntSchemaAdmin(admin.StackedInline):
    model = RestarauntSchema

class RestarauntAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone', 'city']
    exclude = ('actieIdent',)
    inlines = [RestarauntSchemaAdmin]
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


class MenuInPreOrderInLine(admin.TabularInline):
    model = MenuInPreOrder
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaraunt', 'price', 'created_at',]
    list_filter =['restaraunt', 'price',  'created_at',]
    inlines = [MenuInPreOrderInLine]


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaraunt', 'persons', 'table', 'start', 'end', 'name', 'phone']

class СareerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'position']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaraunt', 'date', 'city']

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'description']

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
admin.site.register(Сareer, СareerAdmin)
admin.site.register(Reservation, ReservationAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(Promotion, PromotionAdmin)

admin.site.register(Setting)
admin.site.register(PhotoTable)


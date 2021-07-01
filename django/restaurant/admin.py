from django.contrib import admin
from .models import Category, Feedback, Franchising, MenuInOrder, Menue, Order, Profile, Reservation, Restaraunt, Сareer

admin.site.site_header = 'Respublica administrator'

class MenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'dish', 'category', 'restaraunt']
    list_filter = ['category']
admin.site.register(Menue, MenueAdmin)

class RestarauntAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone']
admin.site.register(Restaraunt, RestarauntAdmin)


class MenuInOrderInLine(admin.TabularInline):
    model = MenuInOrder
    verbose_name = "Меню"
    verbose_name_plural = "Меню"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaraunt', 'price', 'created_at',]
    list_filter =['restaraunt', 'price',  'created_at',]
    inlines = [MenuInOrderInLine]

admin.site.register(Order, OrderAdmin)

admin.site.register(Profile)
admin.site.register(Category)

admin.site.register(Feedback)
admin.site.register(Franchising)
admin.site.register(Сareer)
admin.site.register(Reservation)


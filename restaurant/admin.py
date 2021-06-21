from django.contrib import admin
from .models import Category, MenuInOrder, Menue, Order, Profile, Restaraunt

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


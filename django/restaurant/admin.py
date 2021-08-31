from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Category, Feedback, Franchising, MenuInOrder, Menue, Order, Profile, Reservation, Restaraunt, Сareer, RestarauntSchema

admin.site.site_header = 'Respublica administrator'

class MenueAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'dish', 'category', 'restaraunt']
    list_filter = ['category', 'restaraunt']

    def image_preview(self, obj):
        return mark_safe("<img src='/media/{}'  width='100' />".format(obj.image))
    image_preview.short_description = 'Изображение'
    image_preview.allow_tags = True
admin.site.register(Menue, MenueAdmin)

class RestarauntSchemaAdmin(admin.StackedInline):
    model = RestarauntSchema

class RestarauntAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone']
    inlines = [RestarauntSchemaAdmin]
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


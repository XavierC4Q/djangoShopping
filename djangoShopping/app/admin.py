from django.contrib import admin
from .models import User, Product, ProductDetail, Order
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('display_name', 'email', 'state')}),)

    list_display = (
        'display_name',
        'email',
        'state',
        'date_joined',
        'last_login'
    )


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Order)

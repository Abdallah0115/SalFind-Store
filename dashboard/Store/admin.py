from django.contrib import admin
from django.apps import apps
from .models import Cust, Category , Item , order , CustGroup , ItemRate , Coupon , CouponUser
admin.site.register(Cust)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(order)
admin.site.register(Coupon)
admin.site.register(CouponUser)
admin.site.register(ItemRate)
admin.site.register(CustGroup)


# Register your models here.

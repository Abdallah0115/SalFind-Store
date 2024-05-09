from django.urls import path
from . import views as StoreViews


urlpatterns = [

    path('SalFind',StoreViews.Welcome,name='SalFind'),

    path('',StoreViews.Welcome,name=''),

    path('SalFind/login',StoreViews.Login,name='SalFind/login'),

    path('SalFind/emailValid',StoreViews.Emailenter,name="SalFind/Emailvalid"),

    path('SalFind/Valid',StoreViews.validation,name="SalFind/valid"),

    path('SalFind/sign',StoreViews.Sign,name='SalFind/sign'),

    path('SalFind/Market/<int:id>',StoreViews.Market,name='SaleFind/Market/'),

    path('SalFind/Market/Item/<str:sk>',StoreViews.item,name="SalFind/Market/Item/"),

    path('SalFind/Market/Item/statu/<str:item>',StoreViews.offer,name="SalFind/Market/statu"),

    path('SalFind/Market/logout',StoreViews.Logout_view,name = "SalFind/Market/logout"),

    path('SalFind/me/<str:person>',StoreViews.profile,name = "SalFind/me"),

    path('SalFind/refund/<str:id>',StoreViews.Refund,name = "SalFind/refund"),

    path('SalFind/cancel/<str:id>',StoreViews.cancel,name = "SalFind/cancel"),

    path('SalFind/EditProfile/',StoreViews.edit_profile,name = "SalFind/edProfile"),

    path('SalFind/EditPass/',StoreViews.change_password,name = "SalFind/edPass"),

    path('SalFind/verfyEmail',StoreViews.forgot,name = "SalFind/vefyEmail"),

    path('SalFind/verify',StoreViews.forgotVer,name = "/SalFind/verify"),

    path('SalFind/reset',StoreViews.password_reset_view,name = "SalFind/reset"),
]
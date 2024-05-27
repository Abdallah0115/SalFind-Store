from django.urls import path
from . import views as StoreViews
from django.contrib.auth import views as auth_views


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

    path('SalFind/verfyEmail',auth_views.PasswordResetView.as_view(template_name = "emailValid.html") ,name = "SalFind/vefyEmail"),

    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name = "Done.html"),name = "password_reset_done"),

    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = "confirm.html"),name = "password_reset_confirm"),

    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "complete.html") ,name = "password_reset_complete"),
]
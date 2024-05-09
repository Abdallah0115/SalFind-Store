from django.urls import path
from . import views as DashViews

urlpatterns = [

    path('dash',DashViews.Login,name='dash'),

    path('dash/hello',DashViews.hello,name='dash'),

    path('dash/Analysis/<int:num>',DashViews.Home,name='dash/Analysis'),

    path('dash/addItem',DashViews.AddItem,name='dash/addItem'),

    path('dash/manageItem',DashViews.ManageItem,name='dash/manageItem'),

    path('dash/logout',DashViews.Logout_view, name='dash/logout'),

    path('dash/Edit/<str:it>',DashViews.edItem,name = "dash/Edit"),

    path('dash/manageUser/<int:num>',DashViews.ManageUser,name = "dash/manageUser"),

    path('dash/coupon',DashViews.gift,name = "dash/coupon"),

    path('dash/coupon/generate',DashViews.generatePone,name = "dash/coupon/generate"),

    path('dash/coupon/Edit/<str:item>',DashViews.editPone,name = "dash/coupon/Edit/"),

    path('dash/manageUser/gift/<str:person>',DashViews.giftU,name = "dash/manageUser/gift"),

    path('dash/manageUser/gifts',DashViews.top,name = "dash/manageUser/gifts"),

    path('dash/manageUser/giftsL',DashViews.lower,name = "dash/manageUser/giftsL"),

    path('dash/manageUser/gifts/Cop/<int:num>',DashViews.Gtop,name = "dash/manageUser/gifts/Cop"),

    path('dash/manageUser/gifts/CopL/<int:num>',DashViews.Ltop,name = "dash/manageUser/gifts/CopL"),
]
from unicodedata import name
from django.urls import path
from . import views



urlpatterns=[
        path("",views.index, name="index"),
        path("login.html",views.login_p, name="login"),
        path("register.html",views.register_p, name="register"),
        path("logout/",views.logout_p, name="logout"),
        #path('post/ajax/Message/GET/', views.sender, name = "sender"),
        #path('post/ajax/Message/POST/<slug:slug>/', views.taker, name = "taker"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.layout, name='layout'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('money_transfer/', views.pull_funds_view, name='money_transfer'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('create_coin/', views.create_coin, name='create_coin'),

    path('api/get_ajax_info/', views.get_ajax_info, name='get_ajax_info'),
    path('api/buy-transaction/', views.buy_transaction, name='buy_transaction'),

    path('api/chat/', views.create_message, name='create_message'),
]

from django.urls import path

from .api import playerManager, cardManager

urlpatterns = [
    path('user/login', playerManager.login, name='login'),
    path('user/register', playerManager.register, name='login'),
    path('card/get_cards/<str:user_id>', cardManager.getCards, name='getCards'),
]
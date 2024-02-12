from django.contrib import admin
from .models.player import Player
from .models.card import Card
from .models.log import Log

# Register your models here.
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Log)

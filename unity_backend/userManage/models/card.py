from django.db import models
from userManage.models.player import Player

class Card(models.Model):
    class CardType(models.IntegerChoices):
        FROST_KNIGHT = 0
        FIRE_KNIGHT = 1
        NATURE_KNIGHT = 2
        FROST_WIZARD = 3
        FIRE_WIZARD = 4
        NATURE_WIZARD = 5
        FROST_ARCHER = 6
        FIRE_ARCHER = 7
        NATURE_ARCHER = 8
        WATER_KNIGHT = 9
        WATER_WIZARD = 10
        WATER_ARCHER = 11

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    type = models.IntegerField(choices=CardType.choices)

    class Meta:
        app_label = 'userManage'

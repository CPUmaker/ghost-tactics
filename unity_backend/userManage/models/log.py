from django.db import models
import django.utils.timezone as timezone
from userManage.models.player import Player

class Log(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.player.username

    class Meta:
        app_label = 'userManage'

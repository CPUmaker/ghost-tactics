from django.db import models

class Player(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密')
    )
 
    username = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sexual = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        app_label = 'userManage'

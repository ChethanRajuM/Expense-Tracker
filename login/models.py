from django.db import models

class LoginModel(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

# Create your models here.

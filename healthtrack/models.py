from django.contrib.auth.models import AbstractUser
from django.db import models

#MODEL DE USUÁRIO
class User(AbstractUser):
    pass

# Create your models here.
class BMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
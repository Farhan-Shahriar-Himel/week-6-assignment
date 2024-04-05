from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class AccountModel(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    def __str__(self) -> str:
        return self.user.username
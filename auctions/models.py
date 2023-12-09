from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
class Auction(models.Model):
    title = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.CharField(max_length=1200)
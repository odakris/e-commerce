from django.contrib.auth.models import AbstractUser
from django.db import models

from . import utils

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
    
class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField(max_length=1200)
    # upload = models.FileField(upload_to=utils.user_directory_path)

    def __str__(self):
        return f"{self.title} by {self.seller}"
    
class ImagesUpload(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_img")
    title = models.CharField(max_length=32)
    upload = models.FileField(upload_to=utils.user_directory_path)

    def __str__(self):
        return f"Images for {self.title} item from {self.seller}"
    
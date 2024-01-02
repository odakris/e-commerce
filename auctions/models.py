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
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bid_counter = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.seller}"
    
class ImagesUpload(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_img")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_img", null=True)
    upload = models.FileField(upload_to=utils.user_directory_path, null=True)

    def __str__(self):
        return f"{self.upload}"
    

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction_bid")
    bid_date = models.DateTimeField(auto_now_add=True, null=True)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid} on {self.auction}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="wishlist_auction")
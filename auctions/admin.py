from django.contrib import admin

from .models import User, Category, Auction, ImagesUpload

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(ImagesUpload)

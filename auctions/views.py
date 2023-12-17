from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction, ImagesUpload
from .forms import SellForm

import re


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    images = []
    auction_pk = []

    for img_item in ImagesUpload.objects.all():
        if img_item.auction.pk not in auction_pk:
                images.append(img_item)
                auction_pk.append(img_item.auction.pk)
    
    return render(request, "auctions/categories.html", {
        "title": "All",
        "categories": Category.objects.all(),
        "auctions": Auction.objects.all(),
        "images": images
    })


def sell(request):
    sell_form = SellForm()

    if request.method == "POST":
        sell_form = SellForm(request.POST)
        if sell_form.is_valid():
            title = sell_form.cleaned_data["title"]
            category = sell_form.cleaned_data["category"]
            description = sell_form.cleaned_data["description"]

            new_auction = Auction(
                seller = request.user,
                title = title,
                category = Category.objects.get(pk = category),
                description = description,
            )
            new_auction.save()

            for image in request.FILES.getlist("img-upload"):
                new_img = ImagesUpload(
                    seller = request.user,
                    auction = new_auction,
                    upload = image
                )
                new_img.save()

            return HttpResponseRedirect(reverse("auctions:index"))


    return render(request, "auctions/sell.html", {
        "sell_form": sell_form,
    })




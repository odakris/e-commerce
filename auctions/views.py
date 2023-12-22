from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import OuterRef, Subquery

from .models import User, Category, Auction, ImagesUpload, Bid
from .forms import SellForm, BidForm

from commerce.settings import MEDIA_URL


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
        "all": "All",
        "category": "ALL",
        "categories": Category.objects.all(),
        "auctions": Auction.objects.all(),
        "images": images
    })


def filter(request, filter):
    images = []
    auction_pk = []

    for img_item in ImagesUpload.objects.all():
        if img_item.auction.pk not in auction_pk:
                images.append(img_item)
                auction_pk.append(img_item.auction.pk)
    
    return render(request, "auctions/categories.html", {
        "all": "All",
        "category": filter,
        "categories": Category.objects.all(),
        "auctions": Auction.objects.filter(category=Category.objects.get(name=filter)),
        "images": images
    })
    
# def categories(request):
#     auctions_with_images = Auction.objects.annotate(
#         first_image=Subquery(
#             ImagesUpload.objects.filter(auction=OuterRef('pk')).values('upload')[:1]
#         )
#     )

#     for auction in auctions_with_images:
#         print(auction.first_image)

#     return render(request, "auctions/categories.html", {
#         "title": "All",
#         "categories": Category.objects.all(),
#         "auctions": auctions_with_images,
#         "MEDIA_URL": MEDIA_URL
#     })


def sell(request):
    sell_form = SellForm()

    if request.method == "POST":
        sell_form = SellForm(request.POST)
        if sell_form.is_valid():
            title = sell_form.cleaned_data["title"]
            category = sell_form.cleaned_data["category"]
            description = sell_form.cleaned_data["description"]
            starting_bid = sell_form.cleaned_data["starting_bid"]

            new_auction = Auction(
                seller = request.user,
                title = title,
                category = Category.objects.get(pk = category),
                description = description,
                bid = starting_bid
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


def auction(request, auction_id):
    bid_form = BidForm()
    current_auction = Auction.objects.get(pk=auction_id)
    images = ImagesUpload.objects.filter(auction=current_auction)

    if request.method == "POST":
        if not request.user.is_authenticated: 
            print(request.user)
            return render(request, "auctions/login.html")
        else:

            print(request.user)
            
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.cleaned_data["bid"]

                if bid <= current_auction.bid:
                    return render(request, "auctions/auction.html", {
                        "bid_form": bid_form,
                        "auction": current_auction,
                        "message": "Bid must be higher than current bid"
                    })
                else: 
                    new_bid = Bid(
                        bidder = request.user,
                        auction = current_auction,
                        bid = bid,
                    )
                    new_bid.save()

                    current_auction.bid = bid
                    current_auction.bid_counter = Bid.objects.filter(auction=current_auction).count()
                    print(f"current_auction.bid_counter: {current_auction.bid_counter}")
                    current_auction.save()

                    return render(request, "auctions/auction.html", {
                        "bid_form": bid_form,
                        "auction": current_auction,
                        "images": images,
                        "message": "Bid placed !"
                    })
    

    return render(request, "auctions/auction.html", {
        "bid_form": bid_form,
        "auction": current_auction,
        "images": images
    })




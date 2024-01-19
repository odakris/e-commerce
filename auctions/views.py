from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

# from django.db.models import OuterRef, Subquery

from .models import User, Category, Auction, ImagesUpload, Bid, Wishlist, Comment
from .forms import SellForm, BidForm, CommentForm
from .utils import *


# REvoir images query to do it with Q (better way)


def index(request):
    trending = Auction.objects.order_by("-bid_counter")[:4]
    new = Auction.objects.order_by("-creation_date")[:4]
    images = getFirstImage(ImagesUpload.objects.all())

    return render(request, "auctions/index.html", {
        "trending": trending,
        "new": new,
        "images": images
    })


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
    # Get first image for each auction
    images = getFirstImage(ImagesUpload.objects.all())
    
    return render(request, "auctions/categories.html", {
        "all": "All",
        "category": "ALL",
        "categories": Category.objects.all(),
        "auctions": Auction.objects.filter(active=True).order_by('?'),
        "images": images
    })


def filter(request, filter):
    # Get first image for each auction
    images = getFirstImage(ImagesUpload.objects.all())

    if filter == "all":
        return categories(request)
    
    return render(request, "auctions/categories.html", {
        "all": "All",
        "category": filter,
        "categories": Category.objects.all(),
        "auctions": Auction.objects.filter(active=True, category=Category.objects.get(name=filter)),
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

    # POST REQUESTS 
    if request.method == "POST":
        # get informations form form
        sell_form_data = SellForm(request.POST)
        if sell_form_data.is_valid():
            title = sell_form_data.cleaned_data["title"]
            category = sell_form_data.cleaned_data["category"]
            description = sell_form_data.cleaned_data["description"]
            starting_bid = sell_form_data.cleaned_data["starting_bid"]

            # Create auction into model
            new_auction = Auction(
                seller = request.user,
                title = title,
                category = Category.objects.get(pk = category),
                description = description,
                start_bid = starting_bid
            )
            new_auction.save()

            # Save imported images into model
            for image in request.FILES.getlist("img-upload"):
                new_img = ImagesUpload(
                    seller = request.user,
                    auction = new_auction,
                    upload = image
                )
                new_img.save()

            # Redirect to index
            return HttpResponseRedirect(reverse("auctions:index"))

    # GET REQUESTS
    return render(request, "auctions/sell.html", {
        "sell_form": sell_form,
    })


def auction(request, auction_id):
    bid_form = BidForm()
    comment_form = CommentForm()
    current_auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.filter(auction=current_auction)
    images = ImagesUpload.objects.filter(auction=current_auction)

    # Defined if current auction is user's or not
    closeButton = isUserAuction(request.user, current_auction.pk)

    default_context = {
        "wishlist": "Add To Wishlist",
    }
   
    # Check user wishlist
    if request.user.is_authenticated: 
        is_wishlisted = Wishlist.objects.filter(user=request.user, auction=current_auction)

        if is_wishlisted:
            default_context = {
                    "wishlist": "Remove From Wishlist"
            }
            
            highest_bid = Bid.objects.filter(auction=current_auction).order_by('-bid').first()

            if highest_bid and request.user == highest_bid.bidder:
                default_context['message'] = "You currently got the highest bid !"


    # Check if current auction is user's and replace wishlist button into close auction button
    if request.method == "GET" and isUserAuction(request.user, current_auction.pk):
        default_context = {
            "closeButton": closeButton,
            "closeMessage": "Close Auction"
        }

    context = default_context.copy()

    # POST REQUESTS
    if request.method == "POST":
        # For any POST request user is ask to login of register
        if not request.user.is_authenticated: 
            return render(request, "auctions/login.html")
        else:   
            # Wishlist auction
            if "wishlist" in request.POST:
                context = handle_wishlisting(request, current_auction, is_wishlisted)
            #  Bid auction
            elif "bid" in request.POST:
                # Get bid informations from form
                bid_form_data = BidForm(request.POST)
                context = handle_bidding(request, current_auction, is_wishlisted, bid_form_data, context)
            # Close auction
            elif "close" in request.POST:
                context = handle_auction_closing(request, current_auction, closeButton)
            # Comment auction
            elif "comment" in request.POST:
                comment_form_data = CommentForm(request.POST)
                handle_commenting(request, current_auction, comment_form_data)
                       
    # GET REQUESTS
    return render(request, "auctions/auction.html", {
        "bid_form": bid_form,
        "auction": current_auction,
        "comment_form": comment_form,
        "comments": comments,
        "images": images,
        "active": current_auction.active,
        "context": context
    })

        
def wishlist(request):
    # Get all on going wishlisted auctions
    on_going_wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(auction__active=True))

    # Get all won auctions wishlisted auctions
    won_wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(auction__active=False) & Q(auction__winner=request.user))

    # Get all lost auctions wishlisted auctions
    lost_wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(auction__active=False) & ~Q(auction__winner=request.user))

    images = getFirstImage(ImagesUpload.objects.all())

    return render(request, "auctions/wishlist.html", {
        "ongoing": on_going_wishlist,
        "won": won_wishlist,
        "lost": lost_wishlist,
        "images": images
    })


def myAuctions(request):
    # Get all active auctions posted by current user
    my_active_auctions = Auction.objects.filter(seller=request.user, active=True)
    # Get all non-active auctions posted by current user
    my_closed_auctions = Auction.objects.filter(seller=request.user, active=False)
    # Get auctions images
    images = getFirstImage(ImagesUpload.objects.all())

    return render(request, 'auctions/my_auctions.html', {
        "active": my_active_auctions,
        "closed": my_closed_auctions,
        "images": images
    })


def auction_bids(request, auction_id):
    current_auction = Auction.objects.get(pk=auction_id)
    all_auction_bid = Bid.objects.filter(auction=current_auction).order_by('-bid')

    return render(request, 'auctions/auction_bids.html', {
        "auction": current_auction,
        "bids": all_auction_bid,
    })

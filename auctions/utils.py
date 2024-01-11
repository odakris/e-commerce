from . import models

def user_directory_path(instance, filename):
    # fill will be uploaded to MEDIA_ROOT/user_<id>/item_<id>/<filename>
    return 'user_{0}/item_{1}/{2}'.format(instance.seller.pk, instance.auction.pk, filename)


def all_categories():
    choices = []
    for category in models.Category.objects.all():
        choices.append((category.pk, category.name))

    return choices


def getFirstImage(allImages):
    images = []
    auction_pk = []

    for img_item in allImages:
        if img_item.auction.pk not in auction_pk:
                images.append(img_item)
                auction_pk.append(img_item.auction.pk)

    return images


def isUserAuction(user, auction_id):
    auction = models.Auction.objects.get(pk=auction_id)
    if user == auction.seller:
        return True
    return False

def handle_wishlisting(request, current_auction, is_wishlisted):
    # Add to wishlist
    if request.POST["wishlist"] == "Add To Wishlist":
        # Create wishlist item in model
        new_wishlist = models.Wishlist(
            user = request.user,
            auction = current_auction
        )
        new_wishlist.save()
        context = {
            "message": "This item has been added to your wishlist !",
            "wishlist": "Remove From Wishlist"
        }
    # Remove from wishlist
    elif request.POST["wishlist"] == "Remove From Wishlist":
        # Delete item from wishlist model
        is_wishlisted.delete()
        context = {
            "message": "This item has been removed from your wishlist !",
            "wishlist": "Add To Wishlist"
        }
    
    return context


def handle_bidding(request, current_auction, is_wishlisted, bid_form_data, default_context):
    if bid_form_data.is_valid():
        bid = bid_form_data.cleaned_data["bid"]
        # Handle first bid 
        if current_auction.bid_counter == 0 and bid < current_auction.bid:
            context = {
                "message": "Bid must be at least equal to starting bid",
                "wishlist": default_context["wishlist"]
            }
        # Handle next bids
        elif current_auction.bid_counter != 0 and bid <= current_auction.bid:
            context = {
                "message": "Bid must be higher than current bid",
                "wishlist": default_context["wishlist"]
            }
        # Create bid in model
        else: 
            new_bid = models.Bid(
                bidder = request.user,
                auction = current_auction,
                bid = bid,
            )
            new_bid.save()

            current_auction.bid = bid
            current_auction.bid_counter = models.Bid.objects.filter(auction=current_auction).count()
            current_auction.save()

            # For any bid placed, add item to wishlist if not already
            if not is_wishlisted: 
                new_wishlist = models.Wishlist(
                    user = request.user,
                    auction = current_auction
                )
                new_wishlist.save()

                context = {
                    "message": "Bid placed !",
                    "wishlist": "Remove From Wishlist"
                }
            else: 
                context = {
                    "message": "Bid placed !",
                    "wishlist": default_context["wishlist"]
                }

    return context


def handle_auction_closing(request, current_auction, closeButton):
    # Set auction to non-active
    current_auction.active = False
    current_auction.winner = models.User.objects.get(pk=models.Bid.objects.filter(auction=current_auction).order_by("-bid").values('bidder')[0]['bidder'])
    print(current_auction.winner)
    current_auction.save()

    context = {
        "message": "Bid Closed !",
        "closeButton": closeButton,
    }

    return context


def handle_commenting(request, current_auction, comment_form_data):
    if comment_form_data.is_valid():
        comment = comment_form_data.cleaned_data["comment"]    
        
        #Create new comment
        new_comment = models.Comment(
            user = request.user,
            auction = current_auction,
            comment = comment
        )
        new_comment.save()

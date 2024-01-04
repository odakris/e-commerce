from . import models

def user_directory_path(instance, filename):
    # fill will be uploaded to MEDIA_ROOT/user_<id>/item_<id>/<filename>
    return 'user_{0}/item_{1}/{2}'.format(instance.seller.pk, instance.auction.pk, filename)


def all_categories():
    choices = []
    for category in models.Category.objects.all():
        choices.append((category.pk, category.name))

    return choices


def getFisrtImage(allImages):
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
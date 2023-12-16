from . import models

def user_directory_path(instance, filename):
    # fill will be uploaded to MEDIA_ROOT/user_<id>/item_<id>/<filename>
    return 'user_{0}/item_{1}/{2}'.format(instance.seller.pk, instance.auction.pk, filename)

def all_categories():
    choices = []
    for category in models.Category.objects.all():
        choices.append((category.pk, category.name))

    return choices
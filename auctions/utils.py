from . import models

def user_directory_path(instance, filename):
    # fill will be uploaded to MEDIA_ROOT/user_<id>/<filemane>
    return 'user_{0}_{1}/item_{2}/{4}'.format(instance.seller.pk, instance.seller, instance.title, filename)

def all_categories():
    choices = []
    for category in models.Category.objects.all():
        choices.append((category.pk, category.name))

    print(f"CHOICES: {choices}")
    return choices
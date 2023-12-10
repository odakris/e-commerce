from . import models

def user_directory_path(instance, filename):
    # fill will be uploaded to MEDIA_ROOT/user_<id>/<filemane>
    return 'user_{0}/{1}'.format(instance.seller.id, filename)

def all_categories():
    return models.Category.objects.all()
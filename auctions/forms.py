from django import forms

from . import utils


class SellForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Title", "autocomplete": "off"}))
    category = forms.ChoiceField(label="Category", choices=utils.all_categories())
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea())
    upload = forms.FileField(label="Image")
    #  title = models.CharField(max_length=32)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    # description = models.TextField(max_length=1200)
    # upload = models.FileField(upload_to=utils.user_directory_path)
    # seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
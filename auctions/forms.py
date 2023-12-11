from django import forms

from . import utils


class SellForm(forms.Form):
    title = forms.CharField(label="TITLE", required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title", "autocomplete": "off"}))
    category = forms.ChoiceField(label="CATEGORY", required=True, choices=utils.all_categories())
    description = forms.CharField(label="DESCRIPTION", required=True, widget=forms.Textarea(attrs={"placeholder": "Write a detailed description of your item"}))
    upload = forms.FileField(label="PHOTOS", required=True, widget=forms.FileInput(attrs={"class": "file-btn", "accept": "image/*"}))
    # PRICING

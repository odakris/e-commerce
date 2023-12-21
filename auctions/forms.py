from django import forms

from . import utils

class SellForm(forms.Form):
    title = forms.CharField(label="TITLE", required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title", "autocomplete": "off"}))
    category = forms.ChoiceField(label="CATEGORY", required=True, choices=utils.all_categories())
    description = forms.CharField(label="DESCRIPTION", required=True, widget=forms.Textarea(attrs={"placeholder": "Write a detailed description of your item"}))
    starting_bid = forms.DecimalField(label="STARTING PRICE", required=True, widget=forms.NumberInput(attrs={"min": 1, "class": "form-control", "placeholder": "$", "autocomplete": "off"}))


class BidForm(forms.Form):
    bid = forms.DecimalField(label="BID", widget=forms.NumberInput(attrs={"min": 1, "class": "form-control", "placeholder": "$", "autocomplete": "off"}))
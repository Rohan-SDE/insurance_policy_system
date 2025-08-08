from django import forms
from .models import Customer, Claim

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'claim_amount', 'reason']
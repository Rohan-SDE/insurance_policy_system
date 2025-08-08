from django import forms
from .models import Customer, Claim
from .models import Claim
from .models import Feedback

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'claim_amount', 'reason']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us what you think...'}),
        }

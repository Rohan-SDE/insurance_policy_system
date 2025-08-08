from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'claim_amount', 'reason']

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerForm
from .models import Policy
import stripe
from django.conf import settings
from .models import Policy, Claim
from rest_framework import viewsets
from .serializers import PolicySerializer, ClaimSerializer
from .models import Feedback


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, policy_id):
    policy = CustomerPolicy.objects.get(id=policy_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': policy.policy.policy_name,
                },
                'unit_amount': int(policy.policy.premium_amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )
    return redirect(session.url, code=303)

def policy_list(request):
    policies = Policy.objects.all()
    return render(request, 'insurance/policy_list.html', {'policies': policies})

from .forms import ClaimForm # Create this form
from django.contrib.auth.decorators import login_required

@login_required
def submit_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            # You'll need to associate the claim with the logged-in user's policy
            # This is a simplified example
            claim.save()
            return redirect('claim_success')
    else:
        form = ClaimForm()
    return render(request, 'insurance/submit_claim.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login') # Redirect to login page after successful registration
    else:
        user_form = UserCreationForm()
        customer_form = CustomerForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })

from django.contrib.auth.decorators import login_required
from django.contrib import messages

def policy_list(request):
    policies = Policy.objects.all()
    return render(request, 'insurance/policy_list.html', {'policies': policies})

@login_required
def submit_claim(request):
    # ... (claim view remains the same)
    pass

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.customer = Customer.objects.get(user=request.user)
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'insurance/feedback.html', {'form': form})
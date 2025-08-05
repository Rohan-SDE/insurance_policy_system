from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

# insurance/models.py

class Policy(models.Model):
    policy_name = models.CharField(max_length=200)
    policy_type = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.PositiveIntegerField() # In years
    is_active = models.BooleanField(default=True) # <-- Your new field

    def __str__(self):
        return self.policy_name

class CustomerPolicy(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.customer.user.username}'s {self.policy.policy_name}"

class Claim(models.Model):
    policy = models.ForeignKey(CustomerPolicy, on_delete=models.CASCADE)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    reason = models.TextField()

    def __str__(self):
        return f"Claim for {self.policy}"

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"Feedback from {self.customer.user.username}"
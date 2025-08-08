from django.contrib import admin
from .models import Customer, Feedback, Policy, CustomerPolicy, Claim


admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(CustomerPolicy)
admin.site.register(Claim)
admin.site.register(Feedback)
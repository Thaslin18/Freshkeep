from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    is_consumed = models.BooleanField(default=False)

    def days_until_expiry(self):
        # This is the calculation used by the badges in HTML
        delta = self.expiry_date - timezone.now().date()
        return delta.days

    def status_category(self):
        days = self.days_until_expiry()
        if days <= 3:
            return "RED"
        elif days <= 7:
            return "ORANGE"
        return "NEUTRAL" 

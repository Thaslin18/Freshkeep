from django.db import models
from django.contrib.auth.models import User

class PantryItem(models.Model):
    # Making the user field optional so you can save without logging in
    name = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name


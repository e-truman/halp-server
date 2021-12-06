from django.db import models


class Community_Resource(models.Model):
    contact_type = models.TextField()
    contact = models.TextField()
    street_address = models.TextField()
    phone_number = models.TextField()
    notes = models.TextField()
    geocoded_column = models.TextField()
   
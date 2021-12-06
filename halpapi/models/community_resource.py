from django.db import models


class Community_Resource(models.Model):
    contact = models.TextField() 
    contact_type = models.TextField()
    street_address = models.CharField(max_length=55) 
    phone_number = models.CharField(max_length=10)
    notes = models.TextField()
    # geocoded_column = models.TextField() #how to use location dictionary
   
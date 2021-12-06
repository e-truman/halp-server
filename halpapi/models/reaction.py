from django.db import models

class Reaction(models.Model):
    is_liked = models.BooleanField(default=False) 
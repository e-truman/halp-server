from django.db import models
from django.contrib.auth.models import User


class Reviewer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField()
    created_on = models.DateField()
from django.db import models


class Review_Reaction(models.Model):
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
   
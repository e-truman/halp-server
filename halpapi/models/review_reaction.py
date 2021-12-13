from django.db import models


class Review_Reaction(models.Model):
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE, default=False)
   



  
from django.db import models

class Comment(models.Model):
    review = models.ForeignKey("Review", on_delete=models.CASCADE)
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField()
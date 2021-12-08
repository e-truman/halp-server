from django.db import models


class Review(models.Model):
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    community_resource = models.ForeignKey("Community_Resource", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    content = models.TextField()
    rating = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True) 
    is_published = models.BooleanField(default=False)
    approved = models.BooleanField(default=False) 
    reactions = models.ManyToManyField("Reaction", through="Review_Reaction", related_name="reactions")
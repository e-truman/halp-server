from django.db import models


class Review(models.Model):
    reviewer = models.ForeignKey("Reviewer", on_delete=models.CASCADE)
    community_resource_id = models.ForeignKey("Community_Resource", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    content = models.TextField()
    rating = models.DecimalField
    created_on = models.DateField()
    is_published = models.BooleanField(default=False)
    approved = models.BooleanField(default=False) 
from django.core.management.base import BaseCommand
import requests
from halpapi.models import Community_Resource

class Command(BaseCommand):
    def handle(self, *args, **options): 
        response=requests.get("https://data.nashville.gov/resource/ekvg-j2ns.json")
        for community_resource in response.json(): 
            Community_Resource.objects.create(
                contact = community_resource["contact"],
                contact_type = community_resource.get("contact_type", ""),
                street_address = community_resource.get("street_address", ""),
                phone_number = community_resource.get("phone_number", ""),
                notes = community_resource.get("notes", "")
            )

    
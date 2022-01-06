"""Handle all HTTP requests for posts"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from halpapi.models import Review, Reviewer, Community_Resource, community_resource
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.db.models import Q


class CommunityResourceView(ViewSet):
    """Rare posts"""

    def list(self, request):
        """Handles GET request for all games

        Returns:
            Response -- JSON serialized list of games
        """

        community_resources = Community_Resource.objects.all()


        contact_type = self.request.query_params.get('contact_type', None)
        if contact_type is not None:
            community_resources = community_resources.filter(contact_type=contact_type)

        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            community_resources = Community_Resource.objects.filter(
                Q(contact_type__icontains=search_text) |
                Q(contact__icontains=search_text) |
                Q(street_address__icontains=search_text) |
                Q(notes__icontains=search_text) 
                )

        community_resource_serial = Community_Resource_Serializer(
            community_resources, many=True, context={'request': request})


        return Response(community_resource_serial.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            community_resource = Community_Resource.objects.get(pk=pk)
            serializer = Community_Resource_Serializer(community_resource, context={'request': request})
            #packages data to send back using event serializer at bottom, names it as serializer. result of method call is what is on variable. calling eventserializer and passing in parameters
            return Response(serializer.data) #calling response- a class. passing in the data
        except Exception as ex:
            return HttpResponseServerError(ex) #catches all errors, but want to 





class Community_Resource_Serializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """

    class Meta:
        model = Community_Resource
        fields = ('id', 'contact', 'contact_type', 'street_address', 'phone_number', 'notes')
        depth = 2

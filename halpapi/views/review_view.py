"""Handle all HTTP requests for posts"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from halpapi.models import Review, Reviewer, Community_Resource
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseServerError


class ReviewView(ViewSet):
    """Rare posts"""

    def list(self, request):
        """Handles GET request for all games

        Returns:
            Response -- JSON serialized list of games
        """

        reviews = Review.objects.all()

        # Support filtering games by author
        #   http://localhost:8000/posts?author_id=${authorId}
        #
        # That URL will retrieve all posts by specific user
        reviewer = self.request.query_params.get('reviewer', None)
        if reviewer is not None:
            reviews = reviews.filter(reviewer__id=reviewer)

        posts_serial = ReviewSerializer(
            reviews, many=True, context={'request': request})
        # No need for a context since we're using ModelSerializer.

        return Response(posts_serial.data)

    def create(self, request):
        """Handle POST OPERATIONS

        Returns:
            Response -- JSON serialized post instance
        """

        # Uses the token passed in the 'Authorization' header
        reviewer = Reviewer.objects.get(user=request.auth.user)
        community_resource_id = Community_Resource.objects.get(pk=request.data["communityResourceId"])
        publication_date = date.today()
        try:

            post = Review.objects.create(
                reviewer=reviewer,
                community_resource_id=community_resource_id,
                title=request.data["title"],
                content=request.data["content"],
                rating=request.data["rating"],
                is_published=True,
                approved=True

    
            )
            serializer = ReviewSerializer(post)
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            #packages data to send back using event serializer at bottom, names it as serializer. result of method call is what is on variable. calling eventserializer and passing in parameters
            return Response(serializer.data) #calling response- a class. passing in the data
        except Exception as ex:
            return HttpResponseServerError(ex) #catches all errors, but want to 

    @action(methods=['put'], detail=True)
    def publish(self, request, pk=None):
        """Managing publish / unpublish buttons"""

        review = Review.objects.get(pk=pk)

        if review.is_published is not True:
            review.is_published = True
            review.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            review.is_published = False
            review.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class Community_ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community_Resource
        fields = ('id', 'contact','contact_type', 'street_address', 'phone_number', 'notes' )



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_admin')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic')


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    reviewer = ReviewerSerializer()
    community_resource_id = Community_ResourceSerializer()

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'community_resource_id', 'title', 'content',
                  'rating', 'created_on', 'is_published', 'approved')
        depth = 2


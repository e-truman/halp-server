"""Handle all HTTP requests for posts"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from halpapi.models import Review, Reviewer, Community_Resource, Reaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import HttpResponseServerError


class ReviewView(ViewSet):
    """Halp reviews"""

    def list(self, request):
        """Handles GET request for all games

        Returns:
            Response -- JSON serialized list of games
        """

        reviews = Review.objects.all()

        reviewer = self.request.query_params.get('reviewer', None)
        if reviewer is not None:
            reviews = reviews.filter(reviewer__id=reviewer)

        community_resource = self.request.query_params.get('community_resource', None)
        if community_resource is not None:
            reviews = reviews.filter(community_resource__id=community_resource)

        review_serial = ReviewSerializer(
            reviews, many=True, context={'request': request})
        # No need for a context since we're using ModelSerializer.

        return Response(review_serial.data)

    def create(self, request):
        """Handle POST OPERATIONS

        Returns:
            Response -- JSON serialized review instance
        """

        # Uses the token passed in the 'Authorization' header
        reviewer = Reviewer.objects.get(user=request.auth.user)
        community_resource = Community_Resource.objects.get(pk=request.data["communityResourceId"])
        publication_date = date.today()
        try:

            review = Review.objects.create(
                reviewer=reviewer,
                community_resource=community_resource,
                title=request.data["title"],
                content=request.data["content"],
                rating=request.data["rating"],
                is_published=True,
                approved=True

    
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single review

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

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single review

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        reviewer = Reviewer.objects.get(user=request.auth.user)
        community_resource= Community_Resource.objects.get(pk=request.data["communityResourceId"])

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        review = Review.objects.get(pk=pk)
        review.reviewer = reviewer
        review.community_resource = community_resource
        review.title = request.data["title"]
        review.content = request.data["content"]
        review.rating =request.data["rating"]   
        review.created_on =request.data["createdOn"]
        review.is_published =request.data["isPublished"]
        review.approved =request.data["approved"]

     
        review.save()


        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

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



    @action(methods=['post', 'delete'], detail=True)
    def react(self, request, pk=None):
        """Managing gamers signing up for events"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        reaction = Reaction.objects.get(pk=pk) #how to specify which reaction



        # reviewer = Reviewer.objects.get(user=request.auth.user)
        # community_resource= Community_Resource.objects.get(pk=request.data["communityResourceId"])

        try:
            # Handle the case if the client specifies a game
            # that doesn't exist
           review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response(
                {'message': 'Event does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A gamer wants to sign up for an event
        if request.method == "POST":
            try:
                # Using the attendees field on the event makes it simple to add a gamer to the event
                # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
                review.reactions.add(reaction)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the gamer from the attendees list
                # The method deletes the row in the join table that has the gamer_id and event_id
                review.reactions.remove(reaction)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})



class Community_ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community_Resource
        fields = ('id', 'contact','contact_type', 'street_address', 'phone_number', 'notes' )



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic', 'is_admin')


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializer type
    """
    reviewer = ReviewerSerializer()
    community_resource = Community_ResourceSerializer()

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'community_resource', 'title', 'content',
                  'rating', 'created_on', 'is_published', 'approved', 'reactions')
        depth = 2


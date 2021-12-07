from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from halpapi.models import Reviewer, Reaction
from django.contrib.auth.models import User
from rest_framework.decorators import action


class ReactionView(ViewSet):
    """Rare Publishing"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        reviewer = Reviewer.objects.get(user=request.auth.user)

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            # Create a new Python instance of the Game class
            # and set its properties from what was sent in the
            # body of the request from the client.
            #id, game, organizer, description, date, and time fields


            reaction = Reaction.objects.create(
                label=request.data["label"],
            )
            serializer = ReactionSerializer(is_liked, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            reaction = Reaction.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            #packages data to send back using event serializer at bottom, names it as serializer. result of method call is what is on variable. calling eventserializer and passing in parameters
            return Response(serializer.data) #calling response- a class. passing in the data
        except Exception as ex:
            return HttpResponseServerError(ex) #catches all errors, but want to be specific. can tell what to tell client based on why things not working


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Reaction.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get the current authenticated user
        author = Author.objects.get(user=request.auth.user)
        # Get all game records from the database
        reactions = Reaction.objects.all()



        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request}) #add many=true if you get more than one response
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic', 'is_admin' )

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Reaction
        fields = ('id', 'is_liked')
        depth = 1
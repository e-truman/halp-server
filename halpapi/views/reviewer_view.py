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
from rest_framework.decorators import action

from halpapi.models.review_reaction import Review_Reaction
from halpapi.views.reaction_view import ReactionSerializer



class ReviewerView(ViewSet):
    """Halp reviews"""

    def list(self, request):
        """Handles GET request for all games

        Returns:
            Response -- JSON serialized list of games
        """
        reviewer = Reviewer.objects.get(user=request.auth.user)


        serializer = ReviewerSerializer(
            reviewer, many=False, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized game instance
        """
        

        try:
            reviewer = Reviewer.objects.get(pk=pk)


            # current_user = Reviewer.objects.get(user=request.auth.user)
            # review.current_user_reactions =[]
            # reactions = review.review_reaction_set.all()
            # reactions = reactions.filter(reviewer=current_user)


            serializer = ReviewerSerializer(reviewer, context={'request': request})
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
            user = request.auth.user
            user.delete()
           

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Reviewer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """

        user = request.auth.user
        reviewer = Reviewer.objects.get(user=request.auth.user)
        

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.username = request.data['username']
        user.email = request.data['email']
        reviewer.profile_pic = request.data['profile_pic']
        if request.data.get('password', None):
            user.set_password(request.data['password'])
        user.save()

     
        reviewer.save()


        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic', 'is_admin')




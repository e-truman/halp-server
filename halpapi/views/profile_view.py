from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from halpapi.models import Review, Reviewer, Reaction, Community_Resource, reviewer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action



@api_view(['GET'])
def user_profile(request):
    """Handle GET requests to profile resource

    Returns:
        Response -- JSON representation of user info and events
    """
    reviewer = Reviewer.objects.get(user=request.auth.user)


    current_user = Reviewer.objects.get(user=request.auth.user)
    reviews = Review.objects.all()


    # reviewer = self.request.query_params.get('reviewer', None)
    if reviewer is not None:
        reviews = reviews.filter(reviewer__user=request.auth.user)

        # community_resource = self.request.query_params.get('community_resource', None)
        # if community_resource is not None:
        #     reviews = reviews.filter(community_resource__id=community_resource)

       
        for review in reviews:
            # show all the reactions this user has, don't show as liked if no reaction
            review.current_user_reactions =[]
            reactions = review.review_reaction_set.all()
            reactions = reactions.filter(reviewer=current_user)
            # review.current_user_reactions = reactions.reaction
            for review_reaction in reactions:
                review.current_user_reactions.append(review_reaction.reaction)

            

        review_serial = ReviewSerializer(
            reviews, many=True, context={'request': request})

 
    # current_user = Reviewer.objects.get(user=request.auth.user)
    # TODO: Use the django orm to filter events if the gamer is attending the event
    # review.current_user_reactions =[]
    # reactions = review.review_reaction_set.all()
    # reactions = reactions.filter(reviewer=current_user)

    # TODO: Use the orm to filter events if the gamer is hosting the event
   
    reviewer = ReviewerSerializer(
        reviewer, many=False, context={'request': request})
    
    reviews = ReviewSerializer(
        reviews, many=True)
    
    # Manually construct the JSON structure you want in the response
    profile = {
        "reviewer": reviewer.data,
        "reviews": reviews.data
        # "current_user_reactions": reactions.data
    }

    return Response(profile)

@action(methods=['PUT'], detail=False)
def edit(self, request):
    """Edit the current user's profile"""
    user = request.auth.user
    reviewer = Reviewer.objects.get(user=request.auth.user)
    user.username = request.data['username']
    user.first_name = request.data['first_name']
    user.last_name = request.data['last_name']
    reviewer.profile_pic = request.data['profile_pic']
    # reviewer.profile_pic = request.data['profile_pic']
    if request.data.get('password', None):
        user.set_password(request.data['password'])
    user.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)

class Community_ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Community_Resource
        fields = ('id', 'contact','contact_type', 'street_address', 'phone_number', 'notes' )

@action(methods=['DELETE'], detail=False)
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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic', 'is_admin')

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('is_liked',)

class ReviewSerializer(serializers.ModelSerializer): 
    """JSON serializer for reviews

    Arguments:
        serializer type
    """
    reviewer = ReviewerSerializer()
    community_resource = Community_ResourceSerializer()
    current_user_reactions = ReactionSerializer(many=True)

    class Meta:
        model = Review
        fields = ('id', 'reviewer', 'community_resource', 'title', 'content',
                  'rating', 'created_on', 'is_published', 'approved', 'reactions','current_user_reactions')
        depth = 2









class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class ReviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Reviewer
        fields = ('id', 'user', 'profile_pic', 'is_admin' )
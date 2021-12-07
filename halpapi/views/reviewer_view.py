








# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'username')


# class ReviewerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Reviewer
#         fields = ('id', 'user', 'profile_pic', 'is_admin' )
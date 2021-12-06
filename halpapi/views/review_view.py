"""Handle all HTTP requests for posts"""
from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import Post, Author, Category
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

        posts = Post.objects.all()

        # Support filtering games by author
        #   http://localhost:8000/posts?author_id=${authorId}
        #
        # That URL will retrieve all posts by specific user
        author = self.request.query_params.get('author', None)
        if author is not None:
            posts = posts.filter(author__id=author)

        posts_serial = PostSerializer(
            posts, many=True, context={'request': request})
        # No need for a context since we're using ModelSerializer.

        return Response(posts_serial.data)

    def create(self, request):
        """Handle POST OPERATIONS

        Returns:
            Response -- JSON serialized post instance
        """

        # Uses the token passed in the 'Authorization' header
        author = Author.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["categoryId"])
        publication_date = date.today()
        try:

            post = Post.objects.create(
                author=author,
                category=category,
                title=request.data["title"],
                content=request.data["content"],
                image_url=request.data["imageUrl"],
                publication_date=publication_date,
                is_published=False,
                approved=False
            )
            serializer = PostSerializer(post)
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
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            #packages data to send back using event serializer at bottom, names it as serializer. result of method call is what is on variable. calling eventserializer and passing in parameters
            return Response(serializer.data) #calling response- a class. passing in the data
        except Exception as ex:
            return HttpResponseServerError(ex) #catches all errors, but want to 

    @action(methods=['put'], detail=True)
    def publish(self, request, pk=None):
        """Managing publish / unpublish buttons"""

        post = Post.objects.get(pk=pk)

        if post.is_published is not True:
            post.is_published = True
            post.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            post.is_published = False
            post.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Author
        fields = ('id', 'user')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    author = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 'content',
                  'image_url', 'publication_date', 'is_published', 'approved')
        depth = 2
from rest_framework import serializers
from . import models
import datetime
from rest_framework import status
from rest_framework.response import Response

class HelloSerializer(serializers.Serializer):
    """This will be used to serialize the recipe objects"""

    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for our userporofile objects"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        """Create and return the new data -  doing this because we want to set encrypteed password"""

        user = models.UserProfile(
        email = validated_data['email'],
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class RecipeSerializer(serializers.ModelSerializer):
    """This is the serializer for the recipe models"""

    class Meta:
        model = models.RecipeModel
        fields = ('id', 'title', 'description', 'directions', 'ingredients', 'created_by', 'created_on')
        extra_kwargs = {'created_by':{'read_only':True}, 'created_on':{'read_only':True}}

    def create(self, validated_data):
        """This will create and return the recipe object"""

        recipe = models.RecipeModel(
        title = validated_data['title'],
        description = validated_data['description'],
        directions = validated_data['directions'],
        ingredients = validated_data['ingredients'],
        created_on = datetime.datetime.now()
        )
        recipe.created_on = datetime.datetime.now()
        request = self.context.get('request', None)
        recipe.created_by = request.user
        recipe.save()
        return recipe

    # def list(self):
    #     """This will return only those recipes that are created by the user"""
    #     # return "hello"
    #     request = self.context.get('request', None)
    #     recipies = models.RecipeModel.objects.all().filter(created_by=self.request.user)
    #     return recipies

class FollowingsSerializer(serializers.ModelSerializer):
    """This is the serializer class for following the users"""

    # followed = UserProfileSerializer
    # follower = UserProfileSerializer
    # created_on = serializers.DateTimeField()
    class Meta:
        model = models.FollowingsModel
        fields = ('id', 'followed', 'follower', 'created_on')
        extra_kwargs = {'follower':{'read_only':True}, 'created_on':{'read_only':True}}
        unique_together = ('followed','follower')
    # def save(self):
    #     user = self.context['request'].user
    #     follower = user

    def create(self, validated_data):
        """Custom create method of the followings"""

        following = models.FollowingsModel(
        followed = validated_data['followed']
        )
        following.created_on = datetime.datetime.now()
        request = self.context.get('request', None)
        following.follower = request.user
        existings = models.FollowingsModel.objects.filter(followed=following.followed, follower=following.follower)
        if len(existings) == 0:
            following.save()
            return following
        elif following.follower == following.followed:
            raise serializers.ValidationError({'message':'You Cannot follow yourself'})

        # error = {'message': ",".join('') if len(e.args) > 0 else 'Unknown Error'}
        raise serializers.ValidationError({'message':'Already Exists'})

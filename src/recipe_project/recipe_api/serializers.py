from rest_framework import serializers
from . import models
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
        """Create and return the new data -  doing this because we want to set encrypted password"""

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

    created_by = UserProfileSerializer(read_only=True)
    class Meta:
        model = models.RecipeModel
        fields = ('id', 'title', 'description', 'directions', 'ingredients', 'created_by', 'created_on')
        extra_kwargs = {'created_by':{'read_only':True}, 'created_on':{'read_only':True}}
        use_natural_foreign_keys = True

class FollowingsSerializer(serializers.ModelSerializer):
    """This is the serializer class for following the users"""

    follower = UserProfileSerializer(read_only=True)
    followed = serializers.PrimaryKeyRelatedField(queryset=models.UserProfile.objects.all())

    class Meta:
        model = models.FollowingsModel
        fields = ('id', 'followed', 'follower', 'created_on')
        extra_kwargs = {'follower':{'read_only':True}, 'created_on':{'read_only':True}}
        unique_together = ('followed','follower')

    def create(self, validated_data):
        """Custom create method of the followings"""

        following = models.FollowingsModel(
        followed = validated_data['followed']
        )
        request = self.context.get('request', None)
        following.follower = request.user
        existings = models.FollowingsModel.objects.filter(followed=following.followed, follower=following.follower)
        if len(existings) == 0:
            following.save()
            return following
        elif following.follower == following.followed:
            raise serializers.ValidationError({'message':'You Cannot follow yourself'})

        raise serializers.ValidationError({'message':'You have already followed this user.'})

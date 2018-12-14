from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import viewsets
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handles creating reading and updating profiles
    """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwner ,permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name',)

class UserProfileView(APIView):
    """
    Handles creating reading and updating profiles
    """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwner ,permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name',)

    def get(self, request, format=None):
        """
        Get for users
        """
        users = models.UserProfile.objects.all()
        users_serialized = serializers.UserProfileSerializer(users, many=True)

        return Response(users_serialized.data)


    def post(self, request):
        """
        Manually create a users
        """
        user_serialized = serializers.UserProfileSerializer(data=request.data)
        if user_serialized.is_valid():
             user_serialized.save()
             return Response(user_serialized.data)
        return Response(user_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(APIView):
    """
    This class will handle the details requests for the users
    """

    def get(self, request, pk, format=None):
        """
        Return a single user profiles
        """
        user = self.get_object(pk)
        user_serialized = serializers.UserProfileSerializer(user)
        return Response(user_serialized.data)

    def get_object(self, pk=None):
        """
        Will return a single user onject
        """
        try:
            return models.UserProfile.objects.get(pk=pk)
        except models.UserProfile.DoesNotExist:
            raise Http404

    def put(self, request, pk=None):
        """
        this is manual update of users
        """
        user_serialized = serializers.UserProfileSerializer(data=request.data)

        if user_serialized.is_valid():
            user_serialized.save()
            return Response(user_serialized.data)
        return Response(user_serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginViewSet(viewsets.ViewSet):
    """
    Check Email, pass and return auth token
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use the ObtainAuthToken APIView to validate and create a token
        """

        response = ObtainAuthToken().post(request)
        token = Token.objects.get(key=response.data['token'])
        loginUser = models.UserProfile.objects.get(pk=token.user_id)
        userSerializer = serializers.UserProfileSerializer(loginUser)
        return Response({'token':token.key, 'user':userSerializer.data})

class RecipeViewSet(viewsets.ModelViewSet):
    """
    This is the vieset for recipe models
    """

    serializer_class = serializers.RecipeSerializer

    queryset = models.Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnRecipe, IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', 'directions', 'ingredients',)

    def perform_create(self, serializer):
        """
        This will create a new recipe object in the system
        """

        serializer.save(created_by=self.request.user)

    def list(self, request, pk=None):
        """
        To return the list of recipies according to the followings
        """
        followings = list(models.Followings.objects
                    .filter(follower=request.user)
                    .values_list('followed', flat=True))

        followings.append(request.user)

        queryset = models.Recipe.objects.filter(created_by__in=followings)
        serializer = serializers.RecipeSerializer(queryset, many=True)
        return Response({'recipies': serializer.data})

    def retrieve(self, request, pk=None):
        """
        This will return a single recipe object
        """
        try:

            followings = list(models.Followings.objects
            .filter(follower=request.user).values_list('followed', flat=True))
            followings.append(request.user)
            item = models.Recipe.objects.get(created_by__in=followings, pk=pk)
            recipeSerializer = serializers.RecipeSerializer(item)
            return Response(recipeSerializer.data)

        except ObjectDoesNotExist:
            return Response({'error':'No recipe Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error':'Some error has occoured'}, status=status.HTTP_400_BAD_REQUEST)


class FollowingViewSet(viewsets.ModelViewSet):
    """
    This will be used for following users
    """

    serializer_class = serializers.FollowingsSerializer
    queryset = models.Followings.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'get','delete']


    def list(self, request, pk=None):
        """
        This will return the list of followings
        """

        queryset = models.Followings.objects.filter(follower=request.user)
        serializer = serializers.FollowingsSerializer(queryset, many=True)
        return Response({'followings':serializer.data})

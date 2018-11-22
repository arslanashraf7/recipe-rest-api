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
import datetime
# Create your views here.

class hello_view(APIView):
    """This is the test api view for recipe"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """This is the direct get function when api view is hit"""

        recipe_list = [
        'Recipe 1',
        'Recipe 2',
        'Recipe 3'
        ]


        return Response({'message' : 'Hey Recipe' , 'Data' : recipe_list })

    def post(self, request):
        """Handling new recipe create requests"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello ! {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """This will be used to edit the recipies data"""

        return Response({'Method': 'PUT'})

    def patch(self, request, pk=None):
        """THis will be used to partially update an object"""

        return Response({'Method':'PATCH'})

    def delete(self, request, pk=None):
        """THis will delete the object"""

        return Response({'Method':'DELETE'})

class hello_viewset(viewsets.ViewSet):
    """This is the view set for recipe"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Direct get dunction on the view set"""

        recipies = [
        'Recipe 1',
        'Recipe 2',
        'Recipe3',
        ]

        return Response(
            {'message': 'i will return recipies', 'recipies':recipies})

    def create(self, request):
        """This is used to create the new recipe objects"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request,pk=None):
        """To get the specific recipe object"""

        return Response({'Method':"GET"})

    def update(self, request, pk=None):
        """TO update the recipe object"""

        return Response({'Method':"PUT"})

    def partial_update(self, request, pk=None):
        """TO update the recipe object"""

        return Response({'Method':"PATCH"})

    def destroy(self, request, pk=None):
        """TO update the recipe object"""

        return Response({'Method':"DELETE"})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwner ,permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name',)


class LoginViewSet(viewsets.ViewSet):
    """Check Email, pass and return auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token"""

        return ObtainAuthToken().post(request)

class RecipeViewSet(viewsets.ModelViewSet):
    """This is the vieset for recipe models"""

    serializer_class = serializers.RecipeSerializer

    queryset = models.RecipeModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwner, permissions.UpdateOwnRecipe,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description', 'directions', 'ingredients',)

    def list(self, request, pk=None):
        followings = list(models.FollowingsModel.objects.filter(follower=request.user).values_list('followed', flat=True))
        followings.append(request.user)
        queryset = models.RecipeModel.objects.filter(created_by__in=followings)
        serializer = serializers.RecipeSerializer(queryset, many=True)
        return Response({'recipies': serializer.data})


class FollowingViewSet(viewsets.ModelViewSet):
    """This will be used for following users"""

    serializer_class = serializers.FollowingsSerializer
    queryset = models.FollowingsModel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsOwner,)
    http_method_names = ['post', 'get']

    # def get(self, request, format=None):
    #     """This will return the list of followings"""
    #
    #     followings = models.FollowingsModel.objects.all()
    #     serializer = serializers.FollowingsSerializer(followings, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     """This will create a new following"""
    #
    #     serializer = serializers.FollowingsSerializer(data=request.data)
    #     serializer.follower = request.user
    #     serializer.created_on = datetime.datetime.now()
    #     if serializer.is_valid():
    #         existing = models.FollowingsModel.objects.filter(followed=serializer.data.get('followed'), follower=serializer.data.get('follower'))
    #         if len(existing) == 0:
    #             serializer.create()
    #             return Response(serializer.data , status=status.HTTP_201_CREATED)
    #         return Response({'message':'Already followed this user'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """This is the manager class that will manage the creation and updation of all the users"""

    def create_user(self, email, first_name, last_name, password=None):
        """This function will create normal users f or our system"""
        if not email:
            raise ValueError("Users must have an email address")
        elif not first_name:
            raise ValueError("Users must provide their first name")
        elif not last_name:
            raise ValueError("Users must provide their last name")

        email = self.normalize_email(email)
        user = self.model(email = email, first_name = first_name, last_name = last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    """Just  overriding the base functions here """
    def create_superuser(self, email, first_name, last_name, password):
        """This function will be used to create super users"""

        user = self.create_user(email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """This class is the model class for user profiles"""
    email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_first_name(self):
        """This function returns the first name of user"""

        return self.first_name

    def get_last_name(self):
        """This function will be used to get the last name of the user"""

        return self.last_name

    def get_full_name(self):
        """This method will return the full name of the user"""

        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """This is also the overridden function for base class to provide short name"""

        return self.first_name

    def __str__(self):
        """String operator is being overridden here"""

        return self.email

class RecipeModel(models.Model):
    """This class is the model class for recipies"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    directions = models.CharField(max_length=5000)
    ingredients = models.CharField(max_length=5000)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_on = models.DateTimeField()

    REQUIRED_FIELDS = ['title', 'description']

    def get_title(self):
        """This fun will return recipe title"""

        return self.title

    def get_description(self):
        """This will return recipe description"""

        return self.description

    def get_directions(self):
        """This will return the directions for the recipe"""

        return self.directions

    def get_ingredients(self):
        """This will return the ingredients"""

        return self.ingredients

    def get_created_by(self):
        """This will return the user with which the recipe was created"""

        return self.created_by

    def get_created_on(self):
        """This will return the time when recipe was created"""

        return self.created_on

    def __str__(self):
        """String operator is being overridden here"""

        return self.title

class FollowingsModel(models.Model):
    """This class will hold the followings of the users"""

    id = models.AutoField(primary_key=True)
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    created_on = models.DateTimeField()
    class Meta:
        unique_together = ('follower', 'followed')

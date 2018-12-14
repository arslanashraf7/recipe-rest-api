from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('profile' , views.UserProfileViewSet)
# router.register('profile' , views.UserProfileView.as_view(), 'profile')
router.register('login', views.LoginViewSet, base_name='login')
router.register('recipe' , views.RecipeViewSet)
router.register('followings' , views.FollowingViewSet)

urlpatterns = [
    path('profile/' , views.UserProfileView.as_view()),
    path('profile/<int:pk>/', views.UserProfileDetail.as_view()),
    path('', include(router.urls))
]

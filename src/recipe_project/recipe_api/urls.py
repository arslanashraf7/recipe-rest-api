from django.conf.urls import url
from . import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.hello_viewset, base_name='hello-viewset')
router.register('profile' , views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('recipe' , views.RecipeViewSet)
router.register('followings' , views.FollowingViewSet)

urlpatterns = [
    url(r'^hello-view/', views.hello_view.as_view()),
    # url(r'^followings-view/', views.FollowingView.as_view()),
    url(r'', include(router.urls))
]

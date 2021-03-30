from django.urls import path
from .views import (
    UserRegisterView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    UserActivateView,
    UserListView,

)
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutAllView as KnoxLogoutAllView,
    LogoutView as KnoxLogoutView
)
from rest_framework.authentication import BasicAuthentication

urlpatterns = [
    path("",UserListView.as_view()),
    path("login/",KnoxLoginView.as_view(authentication_classes = (BasicAuthentication,))),
    path("logout/",KnoxLogoutView.as_view()),
    path("logout-all/",KnoxLogoutAllView.as_view()),
    path("register/",UserRegisterView.as_view()),
    path("<int:pk>/",UserDetailView.as_view()),
    path("<int:pk>/update/",UserUpdateView.as_view()),
    path("<int:pk>/delete/",UserDeleteView.as_view()),
    path(r'activate/<id>/<token>/',
        UserActivateView.as_view(), name='activate')

]
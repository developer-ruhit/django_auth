from django.urls import path
from .views import (
    UserRegisterView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
    UserActivateView

)
urlpatterns = [
    path("register/",UserRegisterView.as_view()),
    path("<int:pk>/",UserDetailView.as_view()),
    path("<int:pk>/update/",UserUpdateView.as_view()),
    path("<int:pk>/delete/",UserDeleteView.as_view()),
    path(r'activate/<id>/<token>/',
        UserActivateView.as_view(), name='activate')

]
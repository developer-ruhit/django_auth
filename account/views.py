from django.shortcuts import render,get_object_or_404
from .serializers import UserCreateSerializer,UserDetailSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response

from rest_framework.permissions import (IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny,)
from .permissions import IsAccountOwner
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
import time
import logging

from django.contrib.auth import get_user_model
user = get_user_model()

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


account_activation_token = PasswordResetTokenGenerator()
logging.basicConfig(filename='app_error.log', filemode='w', 
                format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')
class UserRegisterView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = user.objects.all()

    def perform_create(self,serializer):
        print(serializer.validated_data)
        instance = user.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            password = make_password(serializer.validated_data['password']),
            is_active=False
        )
        current_site = get_current_site(self.request)
     
        mail_subject = 'Activate your blog account.'
        message = render_to_string('account_activate_email.html', {
            'user': instance,
            'domain': current_site.domain,
            'id':instance.id,
            'token':account_activation_token.make_token(instance),
        })
        to_email = serializer.validated_data['email']
        email = EmailMessage(
                    mail_subject, message,to=[to_email]
        )
        try:
            email.send()
        except Exception as e:
            instance.delete()
            logging.warning(e)
            raise APIException("Some Error in server side...please try after sometime")
            
            


class UserActivateView(APIView):
    def get(self,request,id,token):
        user = get_object_or_404(get_user_model(),id=id)
        if account_activation_token.check_token(user,token):
            user.is_active=True
            user.save()
        else:
            raise APIException("Invalid token")
        return Response({"message":"Congratulation !!! Your account is activated"})



class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class UserUpdateView(UpdateAPIView):
    serializer_class = UserCreateSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticated,IsAccountOwner,)

class UserDeleteView(DestroyAPIView):
    serializer_class = UserDetailSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticated,IsAccountOwner,)
from django.shortcuts import render,get_object_or_404
from .serializers import UserCreateSerializer,UserDetailSerializer,UserUpdateSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny,IsAdminUser,)
from .permissions import IsAccountOwner
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
import time
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

user = get_user_model()
account_activation_token = PasswordResetTokenGenerator()
logging.basicConfig(filename='app_error.log', filemode='w', 
                format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')


class UserRegisterView(APIView):
    '''
    the view accepts only post method.
    the view creates a user object with is_active=False
    Once it creates a user object then it send a verification mail to user email
    '''
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = user.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            password = make_password(serializer.validated_data['password']),
            is_active=False
        )

        #activation mail send
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
            #if exception delete the instance and log it error.log file
            instance.delete()
            logging.warning(e)
            raise APIException("Some Error in server side...please try after sometime")

     
        return Response({
            "detail":"An email has been sent to your email id for verification",
            "data": serializer.data
            }, status=status.HTTP_201_CREATED)
    


class UserActivateView(APIView):
    '''
    the view handles the activation for user and changes user is_active flag to True
    if the token is valid
    '''
    def get(self,request,id,token):
        user = get_object_or_404(get_user_model(),id=id)
        if account_activation_token.check_token(user,token):
            user.is_active=True
            user.save()
        else:
            raise APIException("Invalid token")
        return Response({"message":"Congratulation !!! Your account is activated"})


class UserListView(generics.ListAPIView):
    '''
    the view provids a list of all users
    the view is accessible only by admin user
    '''
    serializer_class = UserDetailSerializer
    queryset = user.objects.all()
    permission_classes=(IsAdminUser,)


class UserDetailView(generics.RetrieveAPIView):
    '''
    the view provides a particular user detail
    the view is accessible by account owner only
    '''
    serializer_class = UserDetailSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticated,IsAccountOwner)

class UserUpdateView(generics.UpdateAPIView):
    '''
    the view updates the account details
    the view is accessible by account owner only
    '''
    serializer_class = UserUpdateSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticated,IsAccountOwner,)

class UserDeleteView(generics.DestroyAPIView):
    '''
    the view delete the account
    the view is accessible by account owner only
    '''
    serializer_class = UserDetailSerializer
    queryset = user.objects.all()
    permission_classes = (IsAuthenticated,IsAccountOwner,)





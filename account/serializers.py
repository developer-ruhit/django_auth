from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
user = get_user_model()



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = user

        fields = ("first_name","last_name","email","image",)
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = user 
        fields= ("first_name","last_name","email","username","password",)
        extra_kwargs = {
            "password":{"write_only":True}
        }
    
    def validate_email(self,value):
        if not value:
            raise serializers.ValidationError("Email Field must not be empty")

        existing_user = user.objects.filter(email=value)
        if len(existing_user)>0:
            raise serializers.ValidationError("A User already exist with that email")
        return value



    def validate_password(self,value):
        value = value.strip()
        capital_letter_regex = re.compile(".*[A-Z].*")
        numeric_regex = re.compile(".*[0-9].*")



        # minlengthvalidator
        if len(value)<=8:
            raise serializers.ValidationError("Password length must be more than 8 charecters")

        # max_lengthvalidator
        if len(value)>=50:
            raise serializers.ValidationError("Password length must be less than 50 Charecters")

        # Capital letter must exist
        if capital_letter_regex.search(value) is None:
            raise serializers.ValidationError("Password must contain an uppercase letter")

        #numberic charecter existence
        if numeric_regex.search(value) is None:
            raise serializers.ValidationError("Password must contain a number")
        
        #special charected existence...if isalnum true the special char does not exist
        if value.isalnum():
            raise serializers.ValidationError("Password must contain a special charecter")

        return value




class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        exclude = ("password",)
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from .models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        fields = ['full_name','username','password','is_staff']

    def create(self , validate_data):

        user = UserModel(
            username=self.validated_data['username'],
            full_name=self.validated_data['full_name']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user




# class UserLoginSerializer(serializers.Serializer):
#     """
#     Serializer class to authenticate users with email and password.
#     """

#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)



#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import views
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework import status





from .models import CustomUser
from .serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf


class CreateUserView(CreateAPIView):

    model = CustomUser
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer






# class UserLoginAPIView(GenericAPIView):
#     """
#     An endpoint to authenticate existing users using their email and password.
#     """

#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         login_serializer = self.get_serializer(data=request.data,context={'request': request})
#         login_serializer.is_valid(raise_exception=True)
#         user = login_serializer.validated_data
#         # user = login_serializer.validated_data
#         serializer = UserSerializer(user)

#         # data = serializer.data

        # return Response({'message': 'Login successful',
        #     'username': serializer.data['username'],
        #     'password': serializer.data['password'],
        #     'is_staff': serializer.data['is_staff'],}, status=status.HTTP_200_OK )

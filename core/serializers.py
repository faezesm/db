from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserModel
        fields = ['full_name','username','password']

    def create(self , validate_data):

        user = UserModel(
            username=self.validated_data['username'],
            full_name=self.validated_data['full_name']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
        # user = UserModel.objects.create_user(
        #     full_name=self.validated_data['full_name'],
        #     username=self.validated_data['username'],
        #     password=self.validated_data['password'],
        # )
        # return user

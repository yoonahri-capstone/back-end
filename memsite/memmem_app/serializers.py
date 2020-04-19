from rest_framework import serializers
#from .models import Folder
#from .models import Scrap
#from .models import List
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],  validated_data['email'], validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
#    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in")



#class FolderSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Folder
#        fields = ('id', 'user_name', 'folder_name',)


#class ScrapSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Scrap
#        fields = ('id', 'folder_name', 'title', 'url', 'date',)


#class ListSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = List
#        fields = ('id', 'folder_name', 'title', 'thumbnail',)
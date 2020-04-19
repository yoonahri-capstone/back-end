from rest_framework import serializers
from .models import MyUser
#from .models import Folder
#from .models import Scrap
#from .models import List


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'id',
            'name',
            'email')


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
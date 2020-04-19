from django.shortcuts import render

from rest_framework import viewsets
from .models import MyUser
#Folder, Scrap, List
from .serializers import MyUserSerializer
#FolderSerializer, ScrapSerializer, ListSerializer
from rest_framework.decorators import action


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


    #Ex()
    #@action(methods=[''], detail=True, ?)
    #def set_password(self, request, pk=None):



#class FolderViewSet(viewsets.ModelViewSet):
#    queryset = Folder.objects.all()
#    serializer_class = FolderSerializer


#class ScrapViewSet(viewsets.ModelViewSet):
#    queryset = Scrap.objects.all()
#    serializer_class = ScrapSerializer


#class ListViewSet(viewsets.ModelViewSet):
#    queryset = List.objects.all()
#    serializer_class = ListSerializer
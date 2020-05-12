from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth.models import User
from .models import Profile, Folder, Scrap, Memo, Tag

from .serializers import UserSerializer
from .serializers import CreateUserSerializer
from .serializers import LoginUserSerializer
from .serializers import UserFolderSerializer
from .serializers import ScrapSerializer
from .serializers import ScrapListSerializer
#from .serializers import DefaultScrapListSerializer
from .serializers import UrlRequestSerializer
from .serializers import CreateScrapSerializer
from .serializers import CreateTagSerializer
from .serializers import MemoSerializer
from .serializers import TagSerializer
from .serializers import UpdateScrapSerializer

# from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .crawling import crawl_request

from django.http import JsonResponse
#from django.views.generic.base import RedirectView

import requests
import re

# register user
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # if 404 조건들 return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Profile.objects.get_or_create(user=user)
        Folder.objects.get_or_create(user=user, folder_key=0)

        '''
        return Response(
            {
                'user': UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                'token': AuthToken.objects.create(user)[1]
            }
        )
        '''
        return JsonResponse({'status': 200})


# login
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        '''
        return Response(
            {
                'user': UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                # 'token': AuthToken.objects.create(user)[1]
            }
        )
        '''
        return JsonResponse(
            {
                'status': 200,
                'id': UserSerializer(user, context=self.get_serializer_context()
                                     ).data['id']
            }
        )


'''
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
'''


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Get User's Folder List
class FolderViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserFolderSerializer

    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(id=self.kwargs['pk'])


# Get Scrap List (in Folder)
class FolderScrapsViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = ScrapListSerializer

    def get_queryset(self, *args, **kwargs):
        return Folder.objects.filter(user_id=self.kwargs['pk'], folder_key=self.kwargs['folder_key'])

'''
# Get Scrap List (in Default Folder)
class DefaultFolderScrapsViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = DefaultScrapListSerializer

    def get_queryset(self, *args, **kwargs):
        return Folder.objects.filter(user_id=self.kwargs['pk'], folder_key=0)
'''


# Get User Scrap List
class ScrapAllViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer

    def get_queryset(self, *args, **kwargs):
        return Scrap.objects.filter(folder__user=self.kwargs['pk']).order_by('-scrap_id')


'''
class ScrapViewSet(viewsets.ModelViewSet):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer

    def get_queryset(self, *args, **kwargs):
        #return Scrap.objects.filter(folder__user=self.kwargs['pk'], scrap_id=self.kwargs['scrap_pk'])
        return Scrap.objects.filter(scrap_id=self.kwargs['pk'])
'''


regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"


# ADD new url
class CreateScrapAPI(generics.GenericAPIView):
    #serializer_class = CreateScrapSerializer
    serializer_class = UrlRequestSerializer

    def post(self, request, *args, **kwargs):
        # request = [id(user), folder_key, url]
        user = request.POST.get('id', '')
        folder_key = request.POST.get('folder_key', '')
        check = request.POST.get('url', '')
        url = re.findall(regex, check)[0][0]

        response = requests.get(url)
        print(response)# (status_code)

        if Scrap.objects.filter(folder__user=user, url=url).exists():
            return JsonResponse({'message': 'URL EXISTS'}, status=403)

        if response.status_code == 200:
            # crawling = [URL, title, thumbnail, domain] + [tag list..]
            crawling = crawl_request(url)

            if crawling is None:
                return JsonResponse({'message': 'CRAWLING EXCEPTION'}, status=403)
            else:
                crawl_list = []
                tags_list = []
                num = 0

                if len(crawling) > 4:
                    crawl_list = crawling[0:4]
                    tags_list = crawling[4:]
                    num = len(tags_list)
                else:
                    crawl_list = crawling

                # search folder id
                folder_id = Folder.objects.filter(user=user, folder_key=folder_key).values_list('folder_id', flat=True)
                folder_id = folder_id[0]
                
                crawl_data = dict(folder=folder_id,
                                  url=crawl_list[0],
                                  title=crawl_list[1],
                                  thumbnail=crawl_list[2],
                                  domain=crawl_list[3])

                serializer = CreateScrapSerializer(data=crawl_data)
                serializer.is_valid(raise_exception=True)
                scrap = serializer.save()

                if num > 0:
                    tag_to = Scrap.get_id(scrap)
                    for i in range(0, num):
                        tag_data = dict(scrap=tag_to,
                                        tag_text=tags_list[i])
                        tag_serializer = CreateTagSerializer(data=tag_data)
                        tag_serializer.is_valid(raise_exception=True)
                        tag_serializer.save()

                return Response(
                    {
                        'scrap': ScrapSerializer(
                            scrap, context=self.get_serializer_context()
                        ).data
                    }
                )
        else:
            return JsonResponse({'message': 'CANNOT ACCESS (NOT 200)'}, status=403)


class ScrapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer


#임시 update
class UpdateScrap(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scrap.objects.all()
    serializer_class = UpdateScrapSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

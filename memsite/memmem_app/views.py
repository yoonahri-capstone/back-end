from rest_framework import viewsets, permissions, generics, status
from django.contrib.auth.models import User
#from .models import Folder, Scrap, List

from .serializers import UserSerializer
from .serializers import CreateUserSerializer
from .serializers import LoginUserSerializer
#FolderSerializer, ScrapSerializer, ListSerializer
#from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from knox.models import AuthToken


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        #if 404 조건들 return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'user': UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                'token': AuthToken.objects.create(user),
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                'user': UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                'token': AuthToken.objects.create(user),
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#    def list(self, request):
#        queryset = MyUser.objects.all()
#        serializer = MyUserSerializer(queryset, many=True)
#        return Response(serializer.data)

#    def retrieve(self, request, pk=None):
#        queryset = MyUser.objects.all()
#        user = get_object_or_404(queryset, pk=pk)
#        serializer = MyUserSerializer(user)
#        return Response(serializer.data)

    #Ex()
    #@action(methods=[''], detail=True, ?)
    #def set_password(self, request, pk=None):

#class SignUpViewSet(viewsets.ModelViewSet):



#class FolderViewSet(viewsets.ModelViewSet):
#    queryset = Folder.objects.all()
#    serializer_class = FolderSerializer


#class ScrapViewSet(viewsets.ModelViewSet):
#    queryset = Scrap.objects.all()
#    serializer_class = ScrapSerializer


#class ListViewSet(viewsets.ModelViewSet):
#    queryset = List.objects.all()
#    serializer_class = ListSerializer
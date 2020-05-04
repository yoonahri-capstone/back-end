from django.urls import path, include
from .views import MyUserViewSet
from .views import RegistrationAPI
from .views import LoginAPI
from .views import FolderViewSet
from .views import FolderScrapsViewSet
from .views import ScrapAllViewSet
from .views import ScrapViewSet
from .views import CreateScrapAPI

app_name = 'memmem_app'

user_list = MyUserViewSet.as_view({"get": "list"})

user_detail = MyUserViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)

user_folders = FolderViewSet.as_view({"get":"list"})
folder_scraps = FolderScrapsViewSet.as_view({"get":"list"})
user_scraps = ScrapAllViewSet.as_view({"get":"list"})

scrap_detail = ScrapViewSet.as_view({"get":"retrieve", "patch": "partial_update"}) # 수정 필요

urlpatterns = [
    path('auth/register/', RegistrationAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    #path('auth/user/', UserAPI.as_view()),

    path('users/', user_list),
    path('users/<int:pk>/', user_detail, name="note-detail"),
    path('users/<int:pk>/folders/', user_folders),
    path('users/<int:pk>/folders/<int:folder_key>/', folder_scraps),
    path('users/<int:pk>/listall/', user_scraps),
    path('users/<int:pk>/scrap/<int:scrap_pk>/', scrap_detail),

    path('addscrap/', CreateScrapAPI.as_view()),

    path('', include('rest_framework.urls', namespace='rest_framework_category')),
 ]
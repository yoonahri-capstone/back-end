from django.conf.urls import url
from django.urls import path, include
from .views import MyUserViewSet, RegistrationAPI, LoginAPI, UserAPI

app_name = 'memmem_app'

user_list = MyUserViewSet.as_view({"get": "list"})

user_detail = MyUserViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path('users/', user_list),
    url("^users/(?P<pk>[0-9]+)/$", user_detail, name="note-detail"),
    path('auth/register/', RegistrationAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('auth/user/', UserAPI.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
 ]
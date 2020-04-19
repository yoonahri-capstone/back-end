from django.urls import path, include

app_name = 'memmem_app'
urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
 ]
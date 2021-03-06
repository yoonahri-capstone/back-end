from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Client
from .models import Profile
from .models import Folder
from .models import Scrap
from .models import Memo
from .models import Tag
from .models import Place
from .models import Food
from .models import Group


# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,
               ClientInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Folder)
admin.site.register(Scrap)
admin.site.register(Memo)
admin.site.register(Tag)
admin.site.register(Place)
admin.site.register(Food)
admin.site.register(Group)
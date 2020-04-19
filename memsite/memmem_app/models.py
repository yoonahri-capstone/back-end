from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.models import User


class MyUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        """
        Creates and saves a User with the given name, email
        and password.
        """

        if not name:
            raise ValueError('User must have a name')
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=self.name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='user name')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


    #USERNAME_FIELD = 'name' #unique=True



#class User(models.Model):
#    name = models.CharField(max_length=20, unique=True, blank=False)
#    email = models.EmailField(unique=True, blank=False)

#    def __str__(self):
#        return self.name


#class Folder(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
#    folder_name = models.CharField(max_length=50, blank=False)


#class Scrap(models.Model):
#    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, max_length=50, default="default")
#    title = models.CharField(max_length=50)
#    url = models.URLField()
#    date = models.DateField(auto_created=True)
    # resource
    # type


#class List(models.Model):
#    folder_name = models.ForeignKey(Folder, on_delete=models.CASCADE)
#    title = models.ForeignKey(Scrap, on_delete=models.CASCADE)
#    thumbnail = models.ImageField()


#class LogIn(models.Model)
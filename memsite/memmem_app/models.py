from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
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
'''


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='memmem_app/media')

    '''
    @receiver(post_save, sender=User)
    def create_user_profile(self, sender, instance, created, **kwargs):
        if created:
            self.objects.create(user=instance)
            instance.profile.save()
    '''
#    @receiver(post_save, sender=User)
#    def save_user_profile(sender, instance, **kwargs):
#        instance.profile.save()


class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='folders')
    folder_name = models.CharField(max_length=50, blank=False)

    class Meta:
        unique_together = ['user', 'folder_name']

    def __str__(self):
        return self.folder_name


class Scrap(models.Model):
    scrap_id = models.AutoField(primary_key=True, )
    folder = models.ForeignKey(Folder,
                               on_delete=models.CASCADE,
                               related_name='scraps')
    # default
    title = models.CharField(max_length=100)
    url = models.URLField(null=False)
    date = models.DateTimeField(auto_now_add=True,
                            auto_now=False)
    thumbnail = models.URLField()

    class Meta:
        unique_together = ['folder', 'url']
        ordering = ['date']

    def __str__(self):
        return self.url


class Memo(models.Model):
    memo_id = models.AutoField(primary_key=True)
    scrap = models.ForeignKey(Scrap,
                              on_delete=models.CASCADE,
                              related_name='memos')
    memo = models.TextField()

    def __str__(self):
        return self.memo


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    scrap = models.ForeignKey(Scrap,
                              on_delete=models.CASCADE,
                              related_name="tags")
    tag_text = models.CharField(max_length=30)

    def __str__(self):
        return self.tag_text

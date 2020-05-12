from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Folder
from .models import Scrap
from .models import Memo
from .models import Tag


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in")


# Folder
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('folder_key', 'folder_name')


# User's Folder List
class UserFolderSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'folders')

    def get_folders(self, instance):
        folder = instance.folders.all()
        return FolderSerializer(folder, many=True).data


# Scrap List (in Folder)
class ScrapListSerializer(serializers.ModelSerializer):
    scraps = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('folder_key', 'folder_name', 'scraps')

    def get_scraps(self, instance):
        scrap = instance.scraps.all()
        return ScrapSerializer(scrap, many=True).data

'''
# Scrap List (in Default Folder)
class DefaultScrapListSerializer(serializers.ModelSerializer):
    list_all = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('folder_key', 'folder_name', 'list_all')

    def get_list_all(self, instance):
        scrap = instance.list_all.all()
        return ScrapSerializer(scrap, many=True).data
'''


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('memo_id', 'memo')


class CreateMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('scrap',
                  'memo'
                  )

    def create(self, validated_data):
        return Memo.objects.create(**validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_id', 'tag_text')

'''
class UpdateTagSerializer(serializers.ModelSerializer):
    #delete = serializers.SerializerMethodField()
    delete = serializers.BooleanField(required=False)

    class Meta:
        model = Tag
        fields = ('scrap',
                  'tag_text',
                  'delete'
                  )
'''


class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('scrap',
                  'tag_text'
                  )

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)


# scrap 1개 세부정보
class ScrapSerializer(serializers.ModelSerializer):
    memos = serializers.SerializerMethodField()
    #tags = serializers.SerializerMethodField()
    #memos = CreateMemoSerializer(read_only=True, many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Scrap
        fields = ('scrap_id',
                  'folder',
                  'title',
                  'url',
                  'date',
                  'thumbnail',
                  'domain',
                  'memos',
                  'tags',
                  )

    def get_memos(self, instance):
        memo = instance.memos.all()
        return MemoSerializer(memo, many=True).data

    def get_tags(self, instance):
        tag = instance.tags.all()
        return TagSerializer(tag, many=True).data
    '''
    def update(self, instance, validated_data):
        taglist = validated_data.pop('tags')

        scrap_id = validated_data.get('scrap_id', instance.scrap_id)
        instance.scrap_id = scrap_id
        instance.folder = validated_data.get('folder', instance.folder)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        for i in range(0, len(taglist)):
            tag_text = taglist[i].get('tag_text')
            try:
                Tag.objects.filter(scrap=scrap_id, tag_text=tag_text)
            except Tag.DoesNotExist:
                tag_data = dict(scrap=scrap_id,
                                tag_text=tag_text)
                tag_serializer = CreateTagSerializer(data=tag_data)
                tag_serializer.is_valid(raise_exception=True)
                tag_serializer.save()

        return instance
    '''


class UrlRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    folder_key = serializers.IntegerField()
    url = serializers.CharField()


class CreateScrapSerializer(serializers.ModelSerializer):
    memos = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Scrap
        fields = ('folder',
                  'url',
                  'title',
                  'thumbnail',
                  'domain',
                  'memos',
                  'tags')

    def create(self, validated_data):
        return Scrap.objects.create(**validated_data)

    def get_memos(self, instance):
        memo = instance.memos.all()
        return MemoSerializer(memo, many=True).data

    def get_tags(self, instance):
        tag = instance.tags.all()
        return TagSerializer(tag, many=True).data


from rest_framework import serializers
from app1.models import CustomUser, PostData, PostComments

class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class PostSerialize(serializers.ModelSerializer):
    class Meta:
        model = PostData
        fields = '__all__'

    # def get_num_blogs(self, author_id):
    #     return author_id.blogs.count()

class CommentSerialize(serializers.ModelSerializer):
    class Meta:
        model = PostComments
        fields = '__all__'

class CustomPostUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    last_name = serializers.CharField(source='author_id__last_name')
    first_name = serializers.CharField(source='author_id__first_name')
    AutherID = serializers.CharField(source='author_id__id')

class APIsix(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class APIsix2(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()

class GetAuthorBlogsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    published = serializers.BooleanField()
    published_on = serializers.DateField()

class CustomAuthorSearch(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    TotalBlogs = serializers.IntegerField()
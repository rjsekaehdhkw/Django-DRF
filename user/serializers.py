from rest_framework import serializers

from blog.serializers import ArticleSerializer
from blog.serializers import CommentSerializer
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    articles = ArticleSerializer(many=True, source="article_set")
    comments = CommentSerializer(many=True, source="comments_set")
    # 사용자의 게시글 user's article

    class Meta:
        model = UserModel
        fields = ["username", "fullname", "email",
                  "join_date", "userprofile", "articles", "comments"]

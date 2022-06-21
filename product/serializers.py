from rest_framework import serializers
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel
from blog.models import Category as CategoryModel


from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from product.models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail",
                  "description", "created", "exposure_start_date", "exposure_end_date"]

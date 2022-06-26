from django.db.models import Avg
from datetime import datetime
from rest_framework import serializers
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel
from blog.models import Category as CategoryModel


from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from product.models import Product as ProductModel
from product.models import Review as ReviewModel


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.fullname

    class Meta:
        model = ReviewModel
        fields = ["user", "content", "created", "rating"]


class ProductSerializer(serializers.ModelSerializer):

    review = serializers.SerializerMethodField()

    def get_review(self, obj):
        # Product에 있는 모든 리뷰들을 불러옴
        reviews = obj.review_set
        return {
            # 마지막 리뷰를 가져옴
            "last_review": ReviewSerializer(reviews.last()).data,
            "average_rating": reviews.aggregate(Avg("rating"))
        }

    # POST 검증
    def validate(self, data):
        exposure_end_date = data.get("exposure_end_date", "")
        if exposure_end_date and exposure_end_date < datetime.now().date():
            # raise 를 이용하면 에러를 발생 시킬수 있다.
            # ValidationError는 serializers 자체에서 제공해주는 에러
            raise serializers.ValidationError(
                detail={"error": "유효하지 않은 노출 종료 날짜입니다."},
            )
        return data

    # POST 생성
    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()
        product.description += f"\n\n{product.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
        product.save()

        return product

    # POST 수정
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "description":
                value += f"\n\n{instance.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
            setattr(instance, key, value)
        instance.save()
        instance.description = f"{instance.modified.replace(microsecond=0, tzinfo=None)}에 수정되었습니다.\n\n"\
            + instance.description
        instance.save()
        return instance

    class Meta:
        model = ProductModel
        fields = ["user", "thumbnail",
                  "description", "created", "exposure_end_date", "is_active", "price", "review"]

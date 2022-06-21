from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from blog.models import Article as ArticleModel
from user.models import User as UserModel
from DRF_TASK.permissions import RegisteredMoreThanThreeDaysUser

from blog.serializers import ArticleSerializer, CommentSerializer

from datetime import datetime
from DRF_TASK.permissions import IsAdminOrIsAuthenticatedReadOnly


class ArticleView(APIView):
    # 로그인 한 사용자의 게시글 목록 return
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        today = datetime.now()
        articles = ArticleModel.objects.filter(
            exposure_start_date__lte=today,
            exposure_end_date__gte=today,
        ).order_by("id")

        return Response(ArticleSerializer(articles, many=True).data, status=status.HTTP_200_OK)

    # # 로그인 한 사용자의 게시글 목록 return
    # permission_classes = [RegisteredMoreThanThreeDaysUser]

    # def get(self, request):
    #     user = request.user

    #     articles = ArticleModel.objects.filter(user=user)
    #     titles = [article.title for article in articles]  # list 축약 문법

    #     titles = []

    #     for article in articles:
    #         titles.append(article.title)

    #     return Response({"article_list": titles})

    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        contents = request.data.get("contents", "")
        category = request.data.pop("category", [])

        if len(title) <= 5:
            return Response({"error": "타이틀은 5자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        if len(contents) <= 20:
            return Response({"error": "내용은 20자 이상 작성하셔야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not category:
            return Response({"error": "카테고리가 지정되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        article = ArticleModel(
            user=user,
            **request.data
        )
        article.save()
        article.category.add(*category)
        return Response({"message": "성공!!"}, status=status.HTTP_200_OK)

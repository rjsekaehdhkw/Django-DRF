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

from product.serializers import ProductSerializer
from product.models import Product as ProductModel

from datetime import datetime
from django.db.models import Q
# Create your views here.


class ProductView(APIView):
    # product 조회
    def get(self, request):
        today = datetime.now()
        products = ProductModel.objects.filter(
            Q(exposure_end_date__gte=today, is_active=True) |
            Q(user=request.user)
        )

        serialized_data = ProductSerializer(products, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    # product 생성
    def post(self, request):
        request.data['user'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # product 수정

    def put(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

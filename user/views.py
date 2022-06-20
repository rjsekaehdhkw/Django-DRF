from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from django.contrib.auth import login, logout, authenticate

from user.serializers import UserProfileSerializer, UserSerializer, UserSignupSerializer


class UserView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    # 사용자 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입 완료!!"})
        else:
            print(serializer.errors)
            return Response({"message": "가입 실패!!"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})


class UserAPIView(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "login success!!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})

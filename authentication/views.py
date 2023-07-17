from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status, permissions, response
from django.contrib import auth

from django.contrib.auth import authenticate


# Create your views here.


# get logged in user
class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({"user": serializer.data})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    # bypass authentication
    # authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()  # make sure the serializer implements the create method
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    authentication_classes = []

    def post(self, request):
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(
                {"Success": True, "Code": 200, "Details": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid credentials try again"},
            status=status.HTTP_401_UNAUTHORIZED,
        )




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
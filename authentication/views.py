from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions, response
from django.contrib import auth

from django.contrib.auth import authenticate


from rest_framework.decorators import api_view
from .models import User, UserMapping

from django.shortcuts import get_object_or_404


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
    authentication_classes = []

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


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)

    serializer = UserSerializerrrrr(user)
    return Response(serializer.data)


@api_view(["GET"])
def user_list(request, client_id):
    users = User.objects.filter(client_id=client_id)
    serializer = UserSerializerrrrr(users, many=True)  # Use your serializer
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user mapping

# users mapping


@api_view(["GET"])
def get_user_mappings_all(request):
    user_mappings = UserMapping.objects.all()
    serializer = UserMappingSerializer(user_mappings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_user_mappings(request, user_id):
    user_mappings = UserMapping.objects.filter(user__id=user_id)
    serializer = UserMappingSerializer(user_mappings, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_user_mapping(request):
    serializer = UserMappingSerializer(data=request.data)
    if serializer.is_valid():
        property_linked = serializer.validated_data["property_linked"]
        user_id = serializer.validated_data["user"].id

        # Try to get the user mapping instance, or create it if it doesn't exist
        user_mapping, created = UserMapping.objects.get_or_create(
            property_linked=property_linked, user_id=user_id
        )

        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "User mapping already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_user_mapping(request, pk):
    user_mapping = get_object_or_404(UserMapping, pk=pk)

    try:
        user_mapping.delete()
        return Response(
            {"detail": "User mapping deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        return Response(
            {"detail": "An error occurred while deleting the user mapping."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

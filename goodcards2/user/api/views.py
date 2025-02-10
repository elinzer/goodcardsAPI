from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from user.api.serializers import SignUpSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class SignUpView(APIView):
    @api_view(['POST'])
    def signup(request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            body = {'id': user.id, 'username': user.username, 'token': token.key}
            return Response(body, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @api_view(['POST'])
    def login(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data["username"], password=serializer.data["password"])
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                body = {'id': user.id, 'username': user.get_username(), 'token': token.key}
                return Response(body, status=status.HTTP_200_OK)
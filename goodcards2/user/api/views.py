from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from user.api.serializers import SignUpSerializer
from user.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


class SignUpView(APIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

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
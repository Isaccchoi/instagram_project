from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': {
                    'pk': user.pk,
                    'username': user.username,
                    'img_profile': user.img_profile.url if user.img_profile else '',
                    'age': user.age,
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {'data': 'Invalid credentials'}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

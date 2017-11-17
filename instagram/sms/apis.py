from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import SMSSerializer


class SendSMS(APIView):
    def post(self, request):
        serializer = SMSSerializer(request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
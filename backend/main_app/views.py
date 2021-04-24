from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *


class GetMessagesView(APIView):
    """
    Returns messages of current user
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        messages = Message.objects.filter(user=request.user)
        messages = MessageSerializer(messages, context={'request': request}, many=True).data

        return Response(messages)


class IsAuthenticatedView(APIView):
    """
    Returns true if user is authenticated, else - false
    """

    def get(self, request):
        return Response(request.user.is_authenticated)


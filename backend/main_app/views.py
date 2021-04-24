from rest_framework.views import APIView
from rest_framework.response import Response


class IsAuthenticatedView(APIView):
    """
    Returns true if user is authenticated, else - false
    """

    def get(self, request):
        return Response(request.user.is_authenticated)


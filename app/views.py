from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from app.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class Home(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

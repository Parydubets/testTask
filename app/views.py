from django.contrib.auth.models import User
from .models import Restaurant, Category, Menu, Votes
from rest_framework import permissions, viewsets, request, status
from rest_framework_simplejwt import authentication
from app.serializers import UserSerializer, RestaurantSerializer, MenuSerializer,\
    UserRegistrationSerializer, VotesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
# >>> from django.contrib.auth.models import User
# >>> user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

class Home(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}

        return Response(content)


class UserCreateAPI(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is the user to be updated or an admin
        if request.user != user and not user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        query = Restaurant.objects.all()
        serializer = RestaurantSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        data=request.data
        data["user"] = request.user.id
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):

        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data["user"] = request.user.id
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantSerializer(restaurant, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuAPIPublic(APIView):
    authentication_classes = []
    def get(self, request):
        query = Menu.objects.all()
        serializer = MenuSerializer(query, many=True, context={'request': request})
        return Response(serializer.data)


class MenuAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        restaurant_id = request.data.get('restaurant')
        update_time = request.data.get('update_time')
        if not restaurant_id:
            return Response({'error': 'Restaurant ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the restaurant admin or a superuser
        if request.user != restaurant.user and not request.user.is_superuser:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


        data = {"restaurant": restaurant_id,
                "update_time": update_time,
                "upload": request.FILES['upload']}
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            menu = Menu.objects.filter(restaurant_id=id).get(week_day=request.data["week_day"])
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
            # Check if the user is the restaurant admin or a superuser
        if request.user != menu.restaurant.user and not request.user.is_superuser:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        mutable_data = request.data.copy()

        # Modify the copy to preserve the existing restaurant ID
        mutable_data['restaurant'] = menu.restaurant.id

        serializer = MenuSerializer(menu, data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VotesAPI(APIView):
    permission_classes([permissions.IsAuthenticated])
    def get(self, request):
        queryset = Votes.objects.all().order_by('-id')
        serializer = VotesSerializer()
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def post(self):
        pass

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class RestaurantViewSet(viewsets.ModelViewSet):

    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

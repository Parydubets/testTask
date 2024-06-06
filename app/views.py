from django.contrib.auth.models import User
from .models import Restaurant, Menu, Votes
from rest_framework import permissions, viewsets, request, status
from app.serializers import UserSerializer, RestaurantSerializer, MenuSerializer,\
    UserRegistrationSerializer, VotesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count



class Home(APIView):
    # Test view
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

#TODO: add docstrings with required parameters to methods

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
    #Returns restaurants list, creates restaurant, updates restaurant
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
    #Returns available menus for current week day
    authentication_classes = []

    def get(self, request):
        today = timezone.now().strftime('%A').lower()
        menus_today = Menu.objects.filter(week_day=today)
        serializer = MenuSerializer(menus_today, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuAPI(APIView):
    #Creates, updates menu

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
    #Makes a vote for current user
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Votes.objects.all().order_by('-id')
        serializer = VotesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        today = timezone.now().date()
        data = request.data.copy()
        data['vote_user_id'] = request.user.id
        current_day = timezone.now().strftime('%A').lower()
        data["datetime"] = timezone.now()

        try:
            menu = Menu.objects.filter(week_day=current_day).filter(update_time__date=today).exists()
            return Response(menu)
        except Menu.DoesNotExist:
            return Response({'error': 'No menu found for today'}, status=status.HTTP_404_NOT_FOUND)

        if Votes.objects.filter(vote_user_id=request.user.id, datetime__date=timezone.now().date()).exists():
            return Response({'error': 'You have already voted today'}, status=status.HTTP_400_BAD_REQUEST)

        #TODO: allow to vote only for updated today menu

        serializer = VotesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopVoteAPI(APIView):
    #Returns 2 best restaurants by votes for today
    def get(self, request):
        today = timezone.now().date()
        current_day = timezone.now().strftime('%A').lower()
        try:
            menu = Menu.objects.filter(week_day=current_day).exists()
        except Menu.DoesNotExist:
            return Response({'error': 'No menu found for today'}, status=status.HTTP_404_NOT_FOUND)
        top_restaurants = (Votes.objects.filter(datetime__date=today)
                           .values('restaurant_id')
                           .annotate(vote_count=Count('id'))
                           .order_by('-vote_count')[:2])

        restaurant_ids = [restaurant['restaurant_id'] for restaurant in top_restaurants]
        restaurants = Restaurant.objects.filter(id__in=restaurant_ids)

        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class RestaurantViewSet(viewsets.ModelViewSet):

    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

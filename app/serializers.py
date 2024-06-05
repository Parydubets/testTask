from django.contrib.auth.models import User
from .models import Restaurant, Category, Menu, Votes, DAYS
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id','username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [ 'id','username', 'email', 'first_name', 'last_name', 'password']



class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cuisine', 'address', 'user', 'is_active']

    def create(self, validated_data):
        user = validated_data.pop('user')
        restaurant = Restaurant.objects.create(user=user, **validated_data)
        for item in DAYS:
            #TODO:
            #create datetime setup
            Menu.objects.create(restaurant=restaurant, update_time="2024-06-05 23:48:20.63402+03",week_day=item[0])
        return restaurant

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.name = validated_data.get('name', instance.name)
        instance.cuisine = validated_data.get('cuisine', instance.cuisine)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'upload', 'week_day', 'update_time']

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant')
        menu = Menu.objects.create(restaurant=restaurant, **validated_data)
        return menu

    def update(self, instance, validated_data):
        restaurant = validated_data.pop('restaurant')
        instance.restaurant = restaurant

        instance.upload = validated_data.get('upload', instance.upload)
        instance.week_day = validated_data.get('week_day', instance.week_day)
        instance.update_time = validated_data.get('update_time', instance.update_time)
        instance.save()

        return instance


class VotesSerializer(serializers.ModelSerializer):
    vote_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Votes
        fields = ['vote_user_id', 'restaurant_id', 'datetime']

    def create(self, validated_data):
        user = validated_data.pop('vote_user_id')
        restaurant = validated_data.pop('restaurant_id')
        vote = Votes.objects.create(vote_user_id=user, restaurant_id=restaurant, **validated_data)
        return vote

    def update(self, instance, validated_data):
        user = validated_data.pop('vote_user_id')
        restaurant = validated_data.pop('restaurant_id')

        instance.vote_user_id = user
        instance.restaurant_id = restaurant
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.save()

        return instance
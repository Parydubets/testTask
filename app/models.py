from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    admin_id = models.OneToOneField(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(20)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    price = models.IntegerField()
    ingredients = models.TextField()
    mass = models.IntegerField()
    calories = models.IntegerField()
    update_time = models.DateTimeField()


class Votes(models.Model):
    vote_user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    detetime = models.DateTimeField()
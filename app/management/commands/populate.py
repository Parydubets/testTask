from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from app.models import Restaurant, Menu, Votes
from django.core.files import File
from django.utils import timezone
import os
import subprocess

class Command(BaseCommand):
    help = 'Populate database with users and restaurants'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                "username": "admin",
                "password": "adminhere1",
                "first_name": "John",
                "last_name": "Lennon",
                "email": "admin@example.com",
                "is_superuser": True,
                "last_login": "2024-06-05 18:33:40.474778+00"
            },
            {
                "username": "choko_admin",
                "password": "choko_admin1",
                "first_name": "Peter",
                "last_name": "Quill",
                "email": "pquill@example.com",
                "last_login": "2024-06-05 18:33:40.474778+00"
            },
            {
                "username": "qwerty",
                "password": "randompass",
                "first_name": "Peter",
                "last_name": "Maxwell",
                "email": "qwerty@example.com",
                "last_login": "2024-06-05 18:33:40.474778+00"
            },
            {
                "username": "qwerty2",
                "password": "randompass",
                "first_name": "Geralt",
                "last_name": "Of Rivia",
                "email": "geralt@example.com",
                "last_login": "2024-06-05 18:33:40.474778+00"
            },
            {
                "username": "thevoter",
                "password": "randompass",
                "first_name": "Mark",
                "last_name": "Ruffalo",
                "email": "Ruffalo@example.com",
                "last_login": "2024-06-05 18:33:40.474778+00"
            }
        ]
        users = {}
        for user_data in users_data:

            user_data["password"] = make_password(user_data["password"])
            user, created = User.objects.update_or_create(
                username=user_data["username"],
                defaults=user_data
            )
            users[user_data["username"]] = user

        restaurants_data = [
            {
                "name": "John's Cafe",
                "cuisine": "American",
                "address": "123 Main St",
                "user": users["admin"],
                "is_active": True
            },
            {
                "name": "Quill's Grill",
                "cuisine": "Italian",
                "address": "456 Elm St",
                "user": users["choko_admin"],
                "is_active": True
            },
            {
                "name": "Mike`s",
                "cuisine": "English",
                "address": "23 Spring st",
                "user": users["qwerty2"],
                "is_active": True
            }
        ]

        media_path = 'testTask/media/menu.jpg'
        restaurants = {}
        for restaurant_data in restaurants_data:
            user_instance = restaurant_data.pop('user')
            restaurant = Restaurant.objects.update_or_create(user=user_instance, defaults=restaurant_data)
            restaurants[restaurant_data["name"]] = restaurant



        DAYS = (("sunday", "sunday"), ("monday", "monday"), ("tuesday", "tuesday"), ("wednesday", "wednesday"),
                ("thursday", "thursday"), ("friday", "friday"), ("saturday", "saturday"))

        media_path = 'media/menu.jpg'  # Path to the menu image file in the media folder
        for restaurant_id, restaurant_instance in restaurants.items():
            for day in DAYS:


                menu_instance, created = Menu.objects.update_or_create(
                    restaurant_id=restaurant_instance[0].id,
                    week_day=day[0],
                    defaults={'restaurant': restaurant_instance[0]}
                )

                if created:
                    with open(media_path, 'rb') as menu_image:
                        menu_instance.upload.save(os.path.basename(media_path), File(menu_image))
                    menu_instance.save()

        votes_data = [
            {"id": 1,"vote_user_id": users["admin"], "restaurant_id": restaurants["John's Cafe"][0], "datetime": timezone.now()},
            {"id": 2, "vote_user_id": users["choko_admin"], "restaurant_id": restaurants["Quill's Grill"][0],
             "datetime": timezone.now()},
            {"id": 3, "vote_user_id": users["qwerty"], "restaurant_id": restaurants["Mike`s"][0], "datetime": timezone.now()},
            {"id": 4, "vote_user_id": users["qwerty2"], "restaurant_id": restaurants["John's Cafe"][0], "datetime": "2024-06-05 18:33:40.474778+00"},
            {"id": 5, "vote_user_id": users["thevoter"], "restaurant_id": restaurants["Quill's Grill"][0],
             "datetime": timezone.now()},
        ]

        for vote_data in votes_data:
            Votes.objects.create(**vote_data)


        self.stdout.write(self.style.SUCCESS('Successfully populated the database with users and restaurants.'))
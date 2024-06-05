from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from app.models import Restaurant  # Ensure this import matches your app structure

class Command(BaseCommand):
    help = 'Populate database with users and restaurants'

    def handle(self, *args, **kwargs):
        # Create users
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
            }
        ]

        users = {}
        for user_data in users_data:
            # Encrypt the password before saving
            user_data["password"] = make_password(user_data["password"])
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults=user_data
            )

        users = User.objects.all()


        print(users[0].email)

        # Create restaurants
        restaurants_data = [
            {
                "name": "John's Cafe",
                "cuisine": "American",
                "address": "123 Main St",
                "user": users[0],
                "is_active": True
            },
            {
                "name": "Quill's Grill",
                "cuisine": "Italian",
                "address": "456 Elm St",
                "user": users[1],
                "is_active": True
            }
        ]

        for restaurant_data in restaurants_data:
            # Extract user from the restaurant data
            user = restaurant_data.pop('user')
            # Create restaurant with the correct user instance
            Restaurant.objects.get_or_create(user=user, defaults=restaurant_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with users and restaurants.'))

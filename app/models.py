from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone
import urllib
import os


DAYS = (("sunday", "sunday"), ("monday", "monday"), ("tuesday", "tuesday"), ("wednesday", "wednesday"),
        ("thursday", "thursday"), ("friday", "friday"), ("saturday", "saturday"))


class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default=None)
    cuisine = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)



def user_directory_path(instance, filename):
    return "restaurant_{0}/{1}".format(instance.restaurant_id, filename)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to=user_directory_path, blank=True, null=True, default=None)
    week_day = models.CharField(choices=DAYS, default="monday")
    update_time = models.DateTimeField()


    def save(self, *args, **kwargs):
        self.update_time = timezone.now()  # Set update_time to current time
        super().save(*args, **kwargs)


    def cache(self):
        """Store image locally if we have a URL"""

        if self.url and not self.photo:
            result = urllib.urlretrieve(self.url)
            self.photo.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()


class Votes(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    vote_user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
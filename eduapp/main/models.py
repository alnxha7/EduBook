from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class user_profile(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True, null=True)
    password = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    trainer_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='Course')

class Contact(models.Model):
    email = models.EmailField()
    address = models.TextField()

class registered_students(models.Model):
    user = models.CharField(max_length=200)
    email = models.EmailField()
    course = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    amount = models.IntegerField()
    registered_at = models.DateTimeField()
class register_3freeday(models.Model):
    user = models.CharField(max_length=200)
    email = models.EmailField()
    course = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    amount = models.IntegerField()
    registered_at = models.DateTimeField()
    payment_id = models.CharField(max_length=200)

class booking_students(models.Model):
    user = models.CharField(max_length=200)
    email= models.EmailField()
    course = models.CharField(max_length=200)
    price= models.IntegerField()
    duration = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    #end_date = models.DateTimeField()
    payment_id = models.CharField(max_length=200)


class Page(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class PageLock(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    pages = models.ManyToManyField(Page, related_name='locked_pages')
    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.pages.count()} pages locked"




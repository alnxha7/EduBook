from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Contact(models.Model):
    email = models.EmailField()
    address = models.TextField()
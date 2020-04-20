from django.db import models
import datetime


class PersonCollection(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    file_name = models.CharField(max_length=200)
    last_successful_fetch_page = models.IntegerField(default=0)
    data_fetch_complete = models.BooleanField(default=False)


class Person(models.Model):
    person_collection = models.ForeignKey(PersonCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    height = models.CharField(max_length=10)
    mass = models.CharField(max_length=10)
    hair_color = models.CharField(max_length=20)
    skin_color = models.CharField(max_length=20)
    eye_color = models.CharField(max_length=20)
    birth_year = models.CharField(max_length=25)
    gender = models.CharField(max_length=20)
    homeworld = models.CharField(max_length=25)
    date = models.DateField(default=None, blank=True, null=True)

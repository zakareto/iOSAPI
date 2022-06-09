from django.db import models

# Create your models here.

class Videogames(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    rating_id = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videogames'


class Rating(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rating'



class Users(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'Users'


class Cart(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    videogame_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    videogame_name = models.CharField(max_length=50, blank=True, null=True)
    
    videogame_image = models.CharField(max_length=500, blank=True, null=True)
    videogame_price = models.IntegerField(blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'cart'

class Order(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    items = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'order'

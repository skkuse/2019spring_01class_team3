from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.TextField()
    phone_num = models.TextField()

class Country(models.Model):
    cid = models.IntegerField(primary_key=True)
    cname = models.TextField()


class Product(models.Model):
    pid = models.IntegerField(primary_key=True)
    pcode = models.TextField(null=False)
    brand = models.TextField()
    pname = models.TextField()
    category = models.TextField()
    price = models.IntegerField()
    url = models.URLField()
    cid = models.ForeignKey(Country, on_delete = models.CASCADE)

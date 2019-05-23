from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Country(models.Model):
    cid = models.IntegerField(primary_key=True)
    cname = models.TextField()
    short_cname = models.TextField()
    currency = models.TextField()

    def __str__(self):
        return str(self.cid)


class Product(models.Model):
    pcode = models.TextField(null=False)
    brand = models.TextField()
    pname = models.TextField()
    category = models.TextField()
    price = models.IntegerField()
    url = models.URLField()
    cid = models.ForeignKey(Country, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.id) + ", " + self.pname + ", " + str(self.cid)
        
class Favorite (models.Model) :
    fid = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete = models.CASCADE)
    kprice = models.TextField()
    uid = models.ForeignKey(User, on_delete = models.CASCADE)

    def get_pid(self) :
        return self.pid

    def __str__(self) :
        return str(self.fid) + ", "+ str(self.pid)
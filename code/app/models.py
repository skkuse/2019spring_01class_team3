from django.db import models

# Create your models here.
class Country(models.Model):
    cid = models.IntegerField(primary_key=True)
    cname = models.TextField()
    short_cname = models.TextField()

    def __str__(self):
        return str(self.cid) + ", " + self.cname


class Product(models.Model):
    pid = models.IntegerField(primary_key=True)
    pcode = models.TextField(null=False)
    brand = models.TextField()
    pname = models.TextField()
    category = models.TextField()
    price = models.IntegerField()
    url = models.URLField()
    cid = models.ForeignKey(Country, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.pid) + ", " + self.pname + ", " + str(self.cid)

class Favorite (models.Model) :
    fid = models.IntegerField(primary_key=True)
    pid = models.ForeignKey(Product, on_delete = models.CASCADE)
    uid = models.IntegerField()

    def get_pid(self) :
        return self.pid

    def __str__(self) :
        return str(self.fid) + ", "+ str(self.pid)
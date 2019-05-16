from django.db import models

# Create your models here.
class Country(models.Model):
    cid = models.IntegerField(primary_key=True)
    cname = models.TextField()
    short_cmane = models.TextField()

    def __str__(self):
        return self.cname


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
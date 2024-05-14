from django.db import models

# Create your models here.


class Regmodel(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    uname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    img = models.FileField(upload_to="bank_app/static")
    pin = models.IntegerField()
    balance = models.IntegerField()
    ac_num = models.IntegerField()

    def __str__(self):
        return self.uname


class depositamount(models.Model):
    uid = models.IntegerField()
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class withdrawamount(models.Model):
    uid = models.IntegerField()
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class mini(models.Model):
    choice = [
        ('deposit', 'deposit'),
        ('withdraw', 'withdraw')
    ]
    statement = models.IntegerField()


class newsfeed(models.Model):
    topic = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)


class savenew(models.Model):
    uid = models.IntegerField()
    newsid = models.IntegerField()
    topic = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    date = models.DateField()
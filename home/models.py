from django.db import models


class Home(models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='images/')
    title = models.CharField(max_length=100)
    des = models.TextField(blank=True)
    price = models.IntegerField()


class mainBase(models.Model):
    typeOfProduct = models.TextField()
    kg = models.IntegerField(default=0)
    insidePrice = models.IntegerField(default=0)
    outsidePrice = models.IntegerField(default=0)
    totalSum = models.IntegerField(default=0, blank=True)
    date = models.DateField(null=True, auto_now_add=True)
    byWhom = models.TextField(default="")
    changed = models.BooleanField(default=False)

    debt = models.BooleanField(null=True, default=False)
    lastLendDebt = models.IntegerField(null=True, default=0)
    qarzSum = models.IntegerField(null=True, default=0)
    oxirgiQarzBerganVaqti = models.DateField(null=True, auto_now_add=False)
    totalLend = models.IntegerField(null=True, default=0)


class Qarz(models.Model):
    typeOfProduct = models.TextField(null=True)
    kg = models.IntegerField(null=True, default=0)
    orginalPrice = models.IntegerField(null=True, default=0)
    price = models.IntegerField(null=True, default=0)
    totalSum = models.IntegerField(default=0, blank=True)
    date = models.DateField(null=True, auto_now_add=True)
    afterCreateDate = models.DateField(null=True, auto_now_add=True)
    byWhom = models.TextField(null=True, default="")
    changed = models.BooleanField(null=True, default=False)
    debt = models.BooleanField(null=True, default=False)


class InputQarz(models.Model):
    byWhom = models.TextField(null=True, default="")
    qarzSum = models.IntegerField(null=True, default=0)
    oxirgiQarzBerganVaqti = models.DateField(null=True, auto_now_add=False)
    afterCreateDate = models.DateField(null=True, auto_now_add=True)
    totalLend = models.IntegerField(null=True, default=0)


class PayAgent(models.Model):
    who = models.TextField(default='')
    payAgent = models.IntegerField(null=True, default=0)
    lastPayAgent = models.IntegerField(null=True, default=0)
    date = models.DateField(null=True, auto_now_add=True)

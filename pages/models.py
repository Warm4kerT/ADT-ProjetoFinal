from django.db import models

# Create your models here.

class Router(models.Model):
    name = models.CharField(max_length=25)
    localization = models.CharField(max_length=25)
    model = models.CharField(max_length=25)
    ip = models.GenericIPAddressField()
    porta = models.IntegerField(default=22)
    available_space = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=30,default='R@nd0mP@ss')

class Script(models.Model):
    name = models.CharField(max_length=25)
    version = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    compatible_model = models.CharField(max_length=25)
    file = models.FileField(upload_to="scripts")

class Deployment(models.Model):
    date = models.DateField(auto_now=False,auto_now_add=False)
    success = models.BooleanField(default=False)
    router = models.ForeignKey(Router, on_delete=models.PROTECT)
    update = models.ForeignKey(Script, on_delete=models.PROTECT)
    logFile = models.FileField(upload_to="output", default="")
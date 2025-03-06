from django.db import models

class Agreement(models.Model):
    name = models.CharField(max_length=255)

class Resource(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

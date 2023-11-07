from django.db import models

# Create your models here.

class Account(models.Model):
	iban = models.TextField()
	balance = models.IntegerField()

class Donation(models.Model):
    message = models.CharField(max_length=255) 

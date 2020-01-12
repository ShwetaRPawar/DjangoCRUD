from django.db import models

# Create your models here.

class Register(models.Model):
	id=models.AutoField(primary_key=True)
	name = models.CharField(max_length=250)
	address = models.CharField(max_length=500)
	email = models.CharField(max_length=500 ) 
	password = models.CharField(max_length=100)
	confirm_pass = models.CharField(max_length=100)
	status = models.CharField(max_length=100 )
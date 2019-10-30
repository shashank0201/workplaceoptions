from django.db import models
from workplaceOptions import settings
# Create your models here.

class Person(models.Model):
	name=models.CharField(max_length = 255, blank=False, null=False)
	email=models.EmailField(max_length = 255, blank=False, null=False)
	phone=models.CharField(max_length = 10)
	birth_date=models.DateField()

	def __str__(self):
		return self.name

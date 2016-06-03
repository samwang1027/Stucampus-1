from __future__ import unicode_literals

from django.db import models

# Create your models here.

class gpas(models.Model):
   # gid = models.IntegerField()
    profess_id = models.IntegerField()
    course_type = models.CharField(max_length=200)
    course_grade = models.CharField(max_length=200)
    course_need = models.CharField(max_length=200)
 
class plan(models.Model):
   # pid = models.IntegerField()
    profess_id = models.IntegerField()
    course_name = models.CharField(max_length=200)
    total_number = models.CharField(max_length=200)
    credit = models.CharField(max_length=200) 
    credit_type = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200)
    
class professes(models.Model):
   # prid = models.IntegerField()
    year = models.IntegerField()
    collega = models.CharField(max_length=200)
    profess = models.CharField(max_length=200)

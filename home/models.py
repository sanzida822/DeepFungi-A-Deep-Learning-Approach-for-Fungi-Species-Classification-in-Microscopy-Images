from django.db import models
from django.contrib.auth.models import User


class Admin(models.Model):
    name=models.CharField(max_length=150, unique=True)
    email=models.EmailField()
    password=models.CharField(("Password"), max_length=50)

class Doctor(models.Model):
    name=models.CharField(max_length=150)
    gender=models.CharField(max_length=50)
    hospital=models.TextField()
    department=models.CharField(max_length=150)
    mobile=models.CharField(max_length=20)
    email=models.CharField(max_length=50, unique=True)



class Diagnostic(models.Model):
    patient_name=models.CharField(max_length=150)
    mobile=models.CharField(max_length=30)
    gender=models.CharField(max_length=20)
    age=models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='diagnostics')
    sample_date=models.DateField()
    sample_time=models.TimeField()
    report_date= models.DateField()
    report_time=models.TimeField()
    total_cost= models.DecimalField(max_digits=10, decimal_places=2)
    payment=  models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    due= models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20,null=True, blank=True)

class Report(models.Model):
    diagnostic=models.ForeignKey(Diagnostic, on_delete=models.SET_NULL, null=True, related_name='reports')
    status=models.CharField(max_length=20)
    species=models.CharField(max_length=70,null=True)
    description=models.TextField()
    
   

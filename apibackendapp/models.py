from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your models here.

#create a receiver for the signal 'post_save' for the user model
#once it created create a token for that user
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance) #create token for the user





#create a department model class by inheriting the model class
class Department(models.Model):
    #dept id is auto increment and primary key is true
    DepartmentId=models.AutoField(primary_key=True)
    #dept name is a char filed with max char length of 200
    DepartmentName=models.CharField(max_length=200)

    #whenever we try to print the dept object,
    #instead of the memory address of the object,
    #we need to print the name of the department object
    def __str__(self):
        return self.DepartmentName
    
class Employee(models.Model):
    EmployeeId=models.AutoField(primary_key=True)
    EmployeeName=models.CharField(max_length=200)
    Designation=models.CharField(max_length=150)
    DateOfJoining=models.DateField()
    #deptid is a foreign key of the department model
    #on_delete=models.CASCADE means if u delete the dept the delete the whole employee
    DepartmentId =models.ForeignKey(Department, on_delete=models.CASCADE)
    Contact =models.CharField(max_length=150)
    IsActive=models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName

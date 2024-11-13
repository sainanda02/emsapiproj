from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Department,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer
from rest_framework import status

# Creat ur tests here.
#creating new EmployeeViewSetTest class inheriting the APITestCase class
class EmployeeViewSetTest(APITestCase):
    #defining a function to setup some basic data for testing
    def setUp(self):
         #create a sample  object
         self.department = Department.objects.create(DepartmentName="HR")
         #create a sample employee object and assign the department
         self.employee = Employee.objects.create(
              EmployeeName ="Jackie",
              Designation="Kungfu Master",
              DateOfJoining= date(2024,11,13),
              DepartmentId=self.department,
              Contact ="China",
              IsActive = True
         )

        #since we are testing API,we need to create an APIClient
         self.client =APIClient()

    #TEST CASE 1 : Listing Employees
    #defining function to test employee listing api/endpoint
    def test_employee_list(self):
         #the default reverse url for listing modelname-list
        url = reverse('employee-list')
        response= self.client.get(url) #send the api url and get the response

        #get all the employee objects
        employees=Employee.objects.all()
        #create a serializer object from EmployeeSerializer
        serializer= EmployeeSerializer(employees,many=True) #get all the employees

        #check and compare the response against the setup 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data,serializer.data)
        #check if serializer data mathches the actual data format

    #TEST CASE 2 : To get  a particular employee details
    #defining function to test employee listing api/endpoint
    def test_employee_details(self):
         #the default reverse url for listing modelname-list
         #also provide the employee id
        url = reverse('employee-detail',args=[self.employee.EmployeeId])
        response= self.client.get(url) #send the api url and get the response

        #create a serializer object from EmployeeSerializer
        serializer= EmployeeSerializer(self.employee) #get employee detail

        #check and compare the response against the setup 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data,serializer.data)
        #check if serializer data mathches the actual data format

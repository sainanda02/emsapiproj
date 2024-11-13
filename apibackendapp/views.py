from django.shortcuts import render
from rest_framework import viewsets
from .models import Department,Employee
from django.contrib.auth.models import User
from .serializers import EmployeeSerializer,DepartmentSerializer,UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

#create an APIview for signup
class SignupAPIView(APIView):
    permission_classes=[AllowAny] #Signup does not need logging in

    #defining fn to handle signup post data
    #API view cheyumbol post,get,putellam separate cheyanam
    def post(self,request):
        #create an object for the SignupSerializer
        #by giving the data received to its constructor
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            #create a new user if the serializer is valid
            user = serializer.save()
            #after creating a user then create a token for the user
            token,created = Token.objects.get_or_create(user=user) #will give back token object
            #once the user is created,give back the response with usrid,usrname,token,group
            return Response({
                "user_id":user.id,
                "username" : user.username,
                "token" :token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
                #give back the first role id of the user if the role.group exists
            },status=status.HTTP_201_CREATED)
        else:
            #if the serializer is not valid
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


#create an APIview for login
class LoginAPIView(APIView):
    permission_classes=[AllowAny] #Signup does not need logging in

    #defining fn to handle signup post data
    def post(self,request):
        #create an object for the SignupSerializer
        #by giving the data received to its constructor
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            #get the username,password from the validated_data
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            #try to authenticate the user using this username and password
            #if successfully authenticated,it will return back a valid user object

            user = authenticate(request,username=username,password=password)
            if user is not None:
                #get the token for the authenticated user
                token =Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"Success",
                    "username":user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token":token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)#login was success
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid username or password",
            
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED) #login failed
        else:
             #if the serializer is not valid
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)





#create viewset class inheriting the ModelViewSet class
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset=Department.objects.all()       #get all object to the model
    serializer_class=DepartmentSerializer   #and render it using serializer
    #permission_classes=[] #to bypass the authentication
    permission_classes=[IsAuthenticated] # to restrict for login users(13/11 mellill ollathu command aakiyittu ee line command matti koduthu)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()       #get all object to the model
    serializer_class=EmployeeSerializer   #and render it using serializer
    #add search option using employee name or designation(12/11)
    filter_backends=[filters.SearchFilter] #create a search filter
    search_fields=['EmployeeName','Designation'] #add the field to search
    permission_classes=[] #to bypass the authentication
    #permission_classes=[IsAuthenticated] # to restrict for login users

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()       #get all object to the model
    serializer_class=UserSerializer   #and render it using serializer
    #permission_classes=[] #to bypass the authentication
    permission_classes=[IsAuthenticated] # to restrict for login users
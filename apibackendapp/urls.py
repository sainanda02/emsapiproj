from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

#create an instance of the DefaultRouter class
router =DefaultRouter()

#register the mapping for urls and views 
#r for raw string - to escape special chars
router.register(r'departments',views.DepartmentViewSet)
router.register(r'employee',views.EmployeeViewSet)
router.register(r'users',views.UserViewSet)


#creating the urls for the login and signup API views
#They are not viewset,they are api views so it should be addes to the
#url pattern list directly

urlpatterns=[
    path("signup/",views.SignupAPIView.as_view(),name="user-signup"),
    path("login/",views.LoginAPIView.as_view(),name="user-login"),
]
#append the router.urls to the already created uripatterns

urlpatterns += router.urls

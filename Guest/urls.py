from django.urls import path
from Guest import views
app_name='Guest'

urlpatterns = [

     path('UserRegistration/',views.user_registration,name="UserRegistration"),
     path('Login/',views.Login,name="Login"),
     path('',views.Index,name="Index"),
     path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
     path('ViewGallery/',views.ViewGallery,name="ViewGallery"),

     path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
     path('otp/',views.otp,name="otp"),
     path('newpass/',views.newpass,name="newpass"),
     path('Festivals/', views.Festivals, name="Festivals"),
     path('Shivan/', views.Shivan, name="Shivan"),
     path('Kali/', views.Kali, name="Kali"),
     path('Nagam/', views.Nagam, name="Nagam"),
     path('Kurup/', views.Kurup, name="Kurup"),
     path('Chamundi/', views.Chamundi, name="Chamundi"),
]
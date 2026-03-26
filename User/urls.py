from django.urls import path
from User import views
app_name='User'

urlpatterns =[
         path('Myprofile/',views.Myprofile,name="Myprofile"),
         path('Editprofile/',views.Editprofile,name="Editprofile"),
         path('Changepassword/',views.Changepassword,name="Changepassword"),

        path('Homepage/',views.Homepage,name="Homepage"),
        path('ViewGallery/',views.ViewGallery,name="ViewGallery"),
        path('Poojabooking/',views.Poojabooking,name="Poojabooking"), 
        path('ajaxpooja/',views.ajaxpooja,name="ajaxpooja"),


        path('Mybooking/',views.Mybooking,name="Mybooking"),

        path('Payment/<int:bid>',views.Payment,name="Payment"),

        path('ViewPoojas/',views.ViewPoojas,name="ViewPoojas"),
        path('Feedback/',views.Feedback,name="Feedback"),

        path('AddCart/<int:pid>/', views.AddCart, name='AddCart'),

        path('MyCart/', views.MyCart, name="MyCart"),
        path('DelCart/<int:did>', views.DelCart, name="DelCart"),
        path('CartQty/', views.CartQty, name="CartQty"), # No parameters needed in the path itself

       
        path('Shivan/', views.Shivan, name="Shivan"),
        path('Kali/', views.Kali, name="Kali"),
        path('Nagam/', views.Nagam, name="Nagam"),
        path('Kurup/', views.Kurup, name="Kurup"),
        path('Chamundi/', views.Chamundi, name="Chamundi"),
        path('Festivals/', views.Festivals, name="Festivals"),
        path('History/', views.History, name="History"),
        path('Admin/', views.Admin, name="Admin"),
        path('Contact/', views.Contact, name="Contact"),
        path('logout/', views.logout, name="logout"),







]


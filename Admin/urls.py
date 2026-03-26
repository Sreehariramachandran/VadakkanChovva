from django.urls import path
from . import views

app_name = "Admin"

urlpatterns = [
    path("home/", views.admin_home, name="admin_home"),

    path("district/", views.district_manage, name="district_manage"),
    path("district/delete/<int:did>/", views.district_delete, name="district_delete"),
    path("district/edit/<int:did>/", views.district_edit, name="district_edit"),

    path("place/", views.place_manage, name="place_manage"),
    path("place/delete/<int:pid>/", views.place_delete, name="place_delete"),
    path("place/edit/<int:pid>/", views.place_edit, name="place_edit"),

    path("admin/", views.admin_manage, name="admin_manage"),
    path("admin/delete/<int:aid>/", views.admin_delete, name="admin_delete"),
    path("admin/edit/<int:aid>/", views.admin_edit, name="admin_edit"),

    path("deity/", views.deity_manage, name="deity_manage"),
    path("deity/delete/<int:did>/", views.deity_delete, name="deity_delete"),
path('deity_edit/<int:did>/', views.deity_edit, name="deity_edit"),
    path("pooja/", views.pooja_manage, name="pooja_manage"),
    path("pooja/delete/<int:pid>/", views.pooja_delete, name="pooja_delete"),
    path("pooja/edit/<int:pid>/", views.pooja_edit, name="pooja_edit"),

    path("birthstar/", views.birthstar_manage, name="birthstar_manage"),
    path("birthstar/delete/<int:sid>/", views.birthstar_delete, name="birthstar_delete"),
    path("birthstar/edit/<int:sid>/", views.birthstar_edit, name="birthstar_edit"),

    path("gallery/", views.gallery_manage, name="gallery_manage"),
    path("gallery/delete/<int:gid>/", views.gallery_delete, name="gallery_delete"),

    path("notification/", views.notification_manage, name="notification_manage"),
    path("notification/delete/<int:nid>/", views.notification_delete, name="notification_delete"),

    path("bookings/", views.booking_list, name="booking_list"),
   path('booking_complete/<int:bid>/', views.booking_complete, name='booking_complete'),
path('booking_reject/<int:bid>/', views.booking_reject, name='booking_reject'),
       path("Expense/", views.expense, name="Expense"),
       path("logout/", views.logout, name="logout"),
       path("deletefeedback/<int:id>", views.deletefeedback, name="deletefeedback"),

       path("viewfeedback/", views.viewfeedback, name="viewfeedback"),
       path("ajaxgetadmin/", views.ajaxgetadmin, name="ajaxgetadmin"),
]

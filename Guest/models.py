from django.db import models
from Admin.models import tbl_place

class tbl_user(models.Model):
    user_name = models.CharField(max_length=80)
    user_email = models.EmailField(unique=True)
    user_contact = models.CharField(max_length=15)
    user_address = models.TextField()
    user_gender = models.CharField(max_length=10)
    user_dob = models.DateField()

    place_id = models.ForeignKey(tbl_place, on_delete=models.PROTECT)

    user_photo = models.FileField(upload_to="Assets/User/Photos/", blank=True, null=True)

    # store HASHED password (django make_password/check_password)
    user_password = models.CharField(max_length=255)

    user_is_active = models.BooleanField(default=True)
    user_last_login = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name

class tbl_visit(models.Model):
    visit_date=models.DateTimeField(auto_now_add=True)
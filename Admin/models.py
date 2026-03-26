from django.db import models

class tbl_district(models.Model):
    district_name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.district_name


class tbl_place(models.Model):
    place_name = models.CharField(max_length=80)
    district_id = models.ForeignKey(tbl_district, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("place_name", "district_id")

    def __str__(self):
        return f"{self.place_name} ({self.district_id.district_name})"


class tbl_admin(models.Model):
    admin_name = models.CharField(max_length=50)
    admin_email = models.EmailField(unique=True)
    admin_password = models.CharField(max_length=255)  # store hashed
    admin_is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class tbl_deity(models.Model):
    deity_name = models.CharField(max_length=80, unique=True)
    # Added image field (Make sure the upload_to path matches your media settings)
    deity_image = models.FileField(upload_to="Assets/Admin/Deity/", null=True, blank=True)
    deity_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.deity_name


class tbl_birthstar(models.Model):
    birthstar_name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.birthstar_name


class tbl_pooja(models.Model):
    pooja_name = models.CharField(max_length=120)
    pooja_details = models.TextField(blank=True, null=True)

    # IMPORTANT: use DecimalField for money
    pooja_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # duration in minutes (more reliable than text)
    pooja_duration_mins = models.PositiveIntegerField(default=0)

    # optional display time (like "6:00 AM - 7:00 AM")
    pooja_time_label = models.CharField(max_length=80, blank=True, null=True)

    deity_id = models.ForeignKey(tbl_deity, on_delete=models.PROTECT)

    pooja_is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("pooja_name", "deity_id")

    def __str__(self):
        return self.pooja_name


class tbl_gallery(models.Model):
    gallery_file = models.FileField(upload_to="Assets/Admin/Gallery/")
    gallery_description = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


class tbl_notification(models.Model):
    # FIXED: content should be text, not file
    notification_title = models.CharField(max_length=120)
    notification_content = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class tbl_expence(models.Model):
    expence_amount=models.IntegerField()
    expence_date=models.DateField()
    expence_content=models.CharField(max_length=50)
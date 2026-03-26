from django.db import models
from django.utils import timezone
from Admin.models import tbl_pooja, tbl_birthstar
from Guest.models import tbl_user


class tbl_booking(models.Model):
    class BookingStatus(models.IntegerChoices):
        PENDING = 0, "Pending"
        CONFIRMED = 1, "Confirmed"
        CANCELLED = 2, "Cancelled"
        COMPLETED = 3, "Completed"

    booking_number = models.CharField(max_length=30, unique=True)  # ex: TEMPLE2026XXXXX

    # when booking created
    booking_date = models.DateTimeField(auto_now_add=True)

    # pooja date range / single date
    booking_from_date = models.DateField()
    booking_to_date = models.DateField(blank=True, null=True)

    booking_status = models.IntegerField(choices=BookingStatus.choices, default=BookingStatus.PENDING)

    user_id = models.ForeignKey(tbl_user, on_delete=models.PROTECT)

    # totals
    booking_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    booking_notes = models.CharField(max_length=255, blank=True, null=True)

    cancelled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["booking_number"]),
            models.Index(fields=["booking_status"]),
            models.Index(fields=["booking_from_date"]),
        ]

    def __str__(self):
        return self.booking_number


class tbl_booking_item(models.Model):
    class ItemStatus(models.IntegerChoices):
        PENDING = 0, "Pending"
        CONFIRMED = 1, "Confirmed"
        CANCELLED = 2, "Cancelled"
        COMPLETED = 3, "Completed"

    booking_id = models.ForeignKey(tbl_booking, on_delete=models.CASCADE, related_name="items")
    pooja_id = models.ForeignKey(tbl_pooja, on_delete=models.PROTECT)

    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)

    # optional: if multiple same pooja
    quantity = models.PositiveIntegerField(default=1)

    # devotee details per pooja (important in temple bookings)
    devotee_name = models.CharField(max_length=80, blank=True, null=True)
    birthstar_id = models.ForeignKey(tbl_birthstar, on_delete=models.PROTECT, blank=True, null=True)

    # optional extra details
    gotra = models.CharField(max_length=60, blank=True, null=True)
    special_request = models.CharField(max_length=255, blank=True, null=True)

    # schedule per item (time slot)
    pooja_date = models.DateField()
    pooja_time = models.TimeField(blank=True, null=True)

    # store rate snapshot at booking time
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    item_status = models.IntegerField(choices=ItemStatus.choices, default=ItemStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["pooja_date"]),
            models.Index(fields=["item_status"]),
        ]

    def __str__(self):
        return f"{self.booking_id.booking_number} - {self.pooja_id.pooja_name}"


class tbl_payment(models.Model):
    class PaymentStatus(models.IntegerChoices):
        INITIATED = 0, "Initiated"
        SUCCESS = 1, "Success"
        FAILED = 2, "Failed"
        REFUNDED = 3, "Refunded"

    booking_id = models.OneToOneField(tbl_booking, on_delete=models.CASCADE, related_name="payment")

    payment_method = models.CharField(max_length=30, default="online")  # online/cash/upi/card
    payment_provider = models.CharField(max_length=30, blank=True, null=True)  # razorpay/stripe
    payment_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_txn_id = models.CharField(max_length=120, blank=True, null=True)

    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.INITIATED)

    paid_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class tbl_feedback(models.Model):
    user_id = models.ForeignKey(tbl_user, on_delete=models.PROTECT)
    feedback_content=models.CharField(max_length=1000)
    feedback_date=models.DateField(auto_now_add=True)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from Admin.models import *
from User.models import *
from Guest.models import *
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
# =========================
# HOME
# =========================
def admin_home(request):
    date=datetime.now()
    date=date.day
    data=tbl_admin.objects.get(id=request.session['aid'])
    transactions=tbl_payment.objects.all().count()
    income = tbl_payment.objects.aggregate(Sum('payment_amount'))['payment_amount__sum']
    totalorders=tbl_booking_item.objects.all().count()
    totalsales=tbl_booking_item.objects.filter(item_status=1).count()
    totalusers=tbl_user.objects.all().count()
    vistcount=tbl_visit.objects.all().count()
    pooja=tbl_pooja.objects.all().count()

    feedback=tbl_feedback.objects.all()

    #last month earnings

    today = timezone.now().date()

    # First day of this month
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)
    last_month_total = (
        tbl_payment.objects
        .filter(
            payment_status=tbl_payment.PaymentStatus.SUCCESS,
            paid_at__date__range=(first_day_last_month, last_day_last_month)
        )
        .aggregate(total=Sum('payment_amount'))['total'] or 0
    )

    #total expence
    total_expense = (tbl_expence.objects.aggregate(total=Sum('expence_amount'))['total'] or 0)

    return render(request, "Admin/Homepage.html",{'data':data,
                                                  'date':date,
                                                  'transactions':transactions,
                                                  'income':income,
                                                  'last_month_total':last_month_total,
                                                  'totalsales':totalsales,
                                                  'totalorders':totalorders,
                                                  'totalusers':totalusers,
                                                  'vistcount':vistcount,
                                                  'pooja':pooja,
                                                  'feedback':feedback,
                                                  'total_expense':total_expense
                                                  })


from django.shortcuts import render, redirect
from .models import tbl_expence
from datetime import datetime

def expense(request):
    msg = ""

    if request.method == "POST":
        content = request.POST.get("txt_content")
        date = request.POST.get("txt_date")
        amount = request.POST.get("txt_amount")

        tbl_expence.objects.create(
            expence_content=content,
            expence_date=date,
            expence_amount=amount
        )

        msg = "Expense Added Successfully"
        return render(request, "Admin/Expense.html", {
            "msg": msg,
            "total_expense": tbl_expence.objects.all().order_by("-id")
        })

    # GET request
    total_expense = tbl_expence.objects.all().order_by("-id")

    return render(request, "Admin/Expense.html", {
        "total_expense": total_expense
    })


# def Expense(request):
#     if request.method =="POST":
#         Expense_content= request.POST.get("txt_content")
#         Expense_date=request.POST.get("txt_date")               
#         Expense_amount=request.POST.get("txt_amount")

# =========================
# DISTRICT CRUD
# =========================
def district_manage(request):
    if request.method == "POST":
        district_name = (request.POST.get("txt_district") or "").strip()
        if not district_name:
            messages.error(request, "District name required")
            return redirect("Admin:district_manage")

        tbl_district.objects.create(district_name=district_name)
        messages.success(request, "District inserted")
        return redirect("Admin:district_manage")

    districtData = tbl_district.objects.all().order_by("district_name")
    return render(request, "Admin/District.html", {"districtData": districtData})


def district_delete(request, did):
    obj = get_object_or_404(tbl_district, id=did)
    obj.delete()
    messages.success(request, "District deleted")
    return redirect("Admin:district_manage")


def district_edit(request, did):
    editData = get_object_or_404(tbl_district, id=did)

    if request.method == "POST":
        district_name = (request.POST.get("txt_district") or "").strip()
        if not district_name:
            messages.error(request, "District name required")
            return redirect("Admin:district_edit", did=did)

        editData.district_name = district_name
        editData.save()
        messages.success(request, "District updated")
        return redirect("Admin:district_manage")

    return render(request, "Admin/District.html", {"editData": editData})


# =========================
# PLACE CRUD
# =========================
def place_manage(request):
    if request.method == "POST":
        place_name = (request.POST.get("txt_place") or "").strip()
        district_id = request.POST.get("sel_district")

        if not place_name or not district_id:
            messages.error(request, "Place and District required")
            return redirect("Admin:place_manage")

        district = get_object_or_404(tbl_district, id=district_id)

        # ✅ field name is district_id
        tbl_place.objects.create(place_name=place_name, district_id=district)

        messages.success(request, "Place inserted")
        return redirect("Admin:place_manage")

    # ✅ must be district_id (not district)
    placeData = tbl_place.objects.select_related("district_id").all().order_by("place_name")
    districtData = tbl_district.objects.all().order_by("district_name")

    return render(
        request,
        "Admin/Place.html",
        {"districtData": districtData, "placeData": placeData},
    )


def place_delete(request, pid):
    obj = get_object_or_404(tbl_place, id=pid)
    obj.delete()
    messages.success(request, "Place deleted")
    return redirect("Admin:place_manage")


def place_edit(request, pid):
    editData = get_object_or_404(tbl_place, id=pid)
    placeData = tbl_place.objects.select_related("district_id").all().order_by("place_name")
    districtData = tbl_district.objects.all().order_by("district_name")

    if request.method == "POST":
        place_name = (request.POST.get("txt_place") or "").strip()
        district_id = request.POST.get("sel_district")

        if not place_name or not district_id:
            messages.error(request, "Place and District required")
            return redirect("Admin:place_edit", pid=pid)

        editData.place_name = place_name
        editData.district_id = get_object_or_404(tbl_district, id=district_id)
        editData.save()

        messages.success(request, "Place updated")
        return redirect("Admin:place_manage")

    return render(
        request,
        "Admin/Place.html",{"editData": editData, "districtData": districtData, "placeData": placeData},
    )

# =========================
# ADMIN REGISTER CRUD
# =========================
def admin_manage(request):
    if request.method == "POST":
        admin_name = (request.POST.get("txt_name") or "").strip()
        admin_email = (request.POST.get("txt_email") or "").strip()
        admin_password = (request.POST.get("txt_password") or "").strip()

        if not admin_name or not admin_email or not admin_password:
            messages.error(request, "All admin fields required")
            return redirect("Admin:admin_manage")

        tbl_admin.objects.create(
            admin_name=admin_name,
            admin_email=admin_email,
            admin_password=admin_password,  # NOTE: production should hash
        )
        messages.success(request, "Admin inserted")
        return redirect("Admin:admin_manage")

    AdminData = tbl_admin.objects.all().order_by("admin_name")
    return render(request, "Admin/AdminReg.html", {"AdminData": AdminData})


def admin_delete(request, aid):
    obj = get_object_or_404(tbl_admin, id=aid)
    obj.delete()
    messages.success(request, "Admin deleted")
    return redirect("Admin:admin_manage")


def admin_edit(request, aid):
    editData = get_object_or_404(tbl_admin, id=aid)

    if request.method == "POST":
        admin_name = (request.POST.get("txt_name") or "").strip()
        admin_email = (request.POST.get("txt_email") or "").strip()
        admin_password = (request.POST.get("txt_password") or "").strip()

        if not admin_name or not admin_email or not admin_password:
            messages.error(request, "All admin fields required")
            return redirect("Admin:admin_edit", aid=aid)

        editData.admin_name = admin_name
        editData.admin_email = admin_email
        editData.admin_password = admin_password
        editData.save()

        messages.success(request, "Admin updated")
        return redirect("Admin:admin_manage")

    return render(request, "Admin/AdminReg.html", {"editData": editData})

def deity_manage(request):
    if request.method == "POST":
        deity_name = request.POST.get("txt_deity").strip()
        deity_image = request.FILES.get("txt_image") # Now properly capturing the image

        if not deity_name:
            messages.error(request, "Deity name is required.")
            return redirect("Admin:deity_manage")

        # Create the new record including the image
        tbl_deity.objects.create(
            deity_name=deity_name,
            deity_image=deity_image 
        )
        messages.success(request, "Deity inserted successfully.")
        return redirect("Admin:deity_manage")

    d_data = tbl_deity.objects.all().order_by("deity_name")
    return render(request, "Admin/AddDeity.html", {"DeityData": d_data})


def deity_delete(request, did):
    obj = get_object_or_404(tbl_deity, id=did)
    obj.delete()
    messages.success(request, "Deity deleted successfully.")
    return redirect("Admin:deity_manage")


def deity_edit(request, did):
    editData = get_object_or_404(tbl_deity, id=did)
    d_data = tbl_deity.objects.all().order_by("deity_name")

    if request.method == "POST":
        editData.deity_name = request.POST.get("txt_deity").strip()
        
        # Check if a new image was uploaded to replace the old one
        if request.FILES.get("txt_image"):
            editData.deity_image = request.FILES.get("txt_image")
            
        editData.save()
        messages.success(request, "Deity updated successfully.")
        return redirect("Admin:deity_manage")
    
    return render(request, "Admin/AddDeity.html", {
        "editData": editData, 
        "DeityData": d_data 
    })

# =========================
# POOJA CRUD
# =========================
def pooja_manage(request):
    if request.method == "POST":
        name = (request.POST.get("txt_name") or "").strip()
        details = (request.POST.get("txt_details") or "").strip()
        amount = (request.POST.get("txt_amount") or "").strip()

        # your form field txt_time will map to pooja_time_label
        time_label = (request.POST.get("txt_time") or "").strip()

        deity_id = request.POST.get("sel_deity")

        if not name or not amount or not deity_id:
            messages.error(request, "Pooja name, amount and deity required")
            return redirect("Admin:pooja_manage")

        deity = get_object_or_404(tbl_deity, id=deity_id)

        # ✅ correct field names
        tbl_pooja.objects.create(
            pooja_name=name,
            pooja_details=details,
            pooja_amount=amount,
            pooja_time_label=time_label,   # ✅ changed
            deity_id=deity,
        )

        messages.success(request, "Pooja inserted")
        return redirect("Admin:pooja_manage")

    poojaData = tbl_pooja.objects.select_related("deity_id").all().order_by("pooja_name")
    deityData = tbl_deity.objects.all().order_by("deity_name")
    return render(request, "Admin/Addpooja.html", {"poojaData": poojaData, "deityData": deityData})



def pooja_delete(request, pid):
    obj = get_object_or_404(tbl_pooja, id=pid)
    obj.delete()
    messages.success(request, "Pooja deleted")
    return redirect("Admin:pooja_manage")

def pooja_edit(request, pid):
    editData = get_object_or_404(tbl_pooja, id=pid)

    if request.method == "POST":
        name = (request.POST.get("txt_name") or "").strip()
        details = (request.POST.get("txt_details") or "").strip()
        amount = (request.POST.get("txt_amount") or "").strip()
        time_label = (request.POST.get("txt_time") or "").strip()
        deity_id = request.POST.get("sel_deity")

        if not name or not amount or not deity_id:
            messages.error(request, "Pooja name, amount and deity required")
            return redirect("Admin:pooja_edit", pid=pid)

        deity = get_object_or_404(tbl_deity, id=deity_id)

        # ✅ correct field names
        editData.pooja_name = name
        editData.pooja_details = details
        editData.pooja_amount = amount
        editData.pooja_time_label = time_label   # ✅ changed
        editData.deity_id = deity
        editData.save()

        messages.success(request, "Pooja updated")
        return redirect("Admin:pooja_manage")

    poojaData = tbl_pooja.objects.select_related("deity_id").all().order_by("pooja_name")
    deityData = tbl_deity.objects.all().order_by("deity_name")
    return render(
        request,
        "Admin/Addpooja.html",
        {"editData": editData, "poojaData": poojaData, "deityData": deityData},
    )


# =========================
# BIRTHSTAR CRUD
# =========================
def birthstar_manage(request):
    if request.method == "POST":
        birthstar = (request.POST.get("txt_star") or "").strip()
        if not birthstar:
            messages.error(request, "Birthstar required")
            return redirect("Admin:birthstar_manage")

        tbl_birthstar.objects.create(birthstar_name=birthstar)
        messages.success(request, "Birthstar inserted")
        return redirect("Admin:birthstar_manage")

    StarData = tbl_birthstar.objects.all().order_by("birthstar_name")
    return render(request, "Admin/Addbirthstar.html", {"StarData": StarData})


def birthstar_delete(request, sid):
    obj = get_object_or_404(tbl_birthstar, id=sid)
    obj.delete()
    messages.success(request, "Birthstar deleted")
    return redirect("Admin:birthstar_manage")


def birthstar_edit(request, sid):
    editData = get_object_or_404(tbl_birthstar, id=sid)

    if request.method == "POST":
        birthstar = (request.POST.get("txt_star") or "").strip()
        if not birthstar:
            messages.error(request, "Birthstar required")
            return redirect("Admin:birthstar_edit", sid=sid)

        editData.birthstar_name = birthstar
        editData.save()
        messages.success(request, "Birthstar updated")
        return redirect("Admin:birthstar_manage")

    return render(request, "Admin/Addbirthstar.html", {"editData": editData})


# =========================
# GALLERY CRUD
# =========================
def gallery_manage(request):
    if request.method == "POST":
        photo = request.FILES.get("file_photo")
        description = (request.POST.get("txt_description") or "").strip()

        if not photo:
            messages.error(request, "Gallery photo required")
            return redirect("Admin:gallery_manage")

        tbl_gallery.objects.create(gallery_file=photo, gallery_description=description)
        messages.success(request, "Gallery inserted")
        return redirect("Admin:gallery_manage")

    galleryData = tbl_gallery.objects.all().order_by("-id")
    return render(request, "Admin/AddGallery.html", {"galleryData": galleryData})


def gallery_delete(request, gid):
    obj = get_object_or_404(tbl_gallery, id=gid)
    obj.delete()
    messages.success(request, "Gallery deleted")
    return redirect("Admin:gallery_manage")


# =========================
# NOTIFICATION CRUD
# =========================
def notification_manage(request):
    if request.method == "POST":
        title = (request.POST.get("txt_title") or "").strip()
        content = (request.POST.get("txt_content") or "").strip()

        if not title or not content:
            messages.error(request, "Title and Content required")
            return redirect("Admin:notification_manage")

        # ✅ do NOT set notification_date (auto_now_add handles it)
        tbl_notification.objects.create(
            notification_title=title,
            notification_content=content,
        )

        messages.success(request, "Notification inserted")
        return redirect("Admin:notification_manage")

    n_data = tbl_notification.objects.all().order_by("-id")
    return render(request, "Admin/AddNotifications.html", {"n_data": n_data})

def notification_delete(request, nid):
    obj = get_object_or_404(tbl_notification, id=nid)
    obj.delete()
    messages.success(request, "Notification deleted")
    return redirect("Admin:notification_manage")
def booking_list(request):
    # Retrieve all bookings EXCEPT active shopping carts (status 0)
    # prefetch_related efficiently grabs all the nested data in one fast query
    bookingData = tbl_booking.objects.select_related("user_id").prefetch_related(
        "items__pooja_id__deity_id", 
        "items__birthstar_id"
    ).exclude(booking_status=0).order_by("-id")
    
    return render(request, "Admin/ViewBooking.html", {"bookingData": bookingData})


def booking_reject(request, bid):
    # Update Booking Status to 2 (Cancelled)
    booking = tbl_booking.objects.get(id=bid)
    booking.booking_status = 2
    booking.cancelled_at = timezone.now()
    booking.save()
    
    # Update all related items to Cancelled
    items = tbl_booking_item.objects.filter(booking_id=booking)
    for item in items:
        item.item_status = 2
        item.save()
        
    messages.success(request, "Booking Cancelled Successfully.")
    return redirect("Admin:booking_list") 


def booking_complete(request, bid):
    # Update Booking Status to 3 (Completed)
    booking = tbl_booking.objects.get(id=bid)
    booking.booking_status = 3
    booking.save()
    
    # Update all related items to Completed
    items = tbl_booking_item.objects.filter(booking_id=booking)
    for item in items:
        item.item_status = 3
        item.save()
        
    messages.success(request, "Booking Marked as Completed.")
    return redirect("Admin:booking_list")


def logout(request):
    del request.session['aid']
    return redirect("Guest:Login")

def deletefeedback(request, id):
    tbl_feedback.objects.get(id=id).delete()
    return redirect('Admin:admin_home')

def viewfeedback(request):
    feeddata = tbl_feedback.objects.all()
    return render(request,"Admin/Feedback.html",{"feeddata":feeddata})

def ajaxgetadmin(request):
    admin = tbl_admin.objects.get(id=request.session['aid'])
    return JsonResponse({"admindata":admin.admin_name})
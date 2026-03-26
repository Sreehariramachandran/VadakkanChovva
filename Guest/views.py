from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.


def user_registration(request):
    # Fetching data for the dropdowns
    districts = tbl_district.objects.all()
    places = tbl_place.objects.all()

    if request.method == "POST":
        # Capturing text and selection data
        name = request.POST.get('txt_name')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')
        address = request.POST.get('txt_address')
        gender = request.POST.get('radio_gender')
        dob = request.POST.get('date_dob')

        pid , create = tbl_place.objects.get_or_create(
            place_name = request.POST.get('sel_place'),
            district_id = tbl_district.objects.get(id=request.POST.get('sel_district'))
        )
        place_id = tbl_place.objects.get(id=pid.id)
        
        # Capturing File data
        photo = request.FILES.get('file_photo')
        
        password = request.POST.get('txt_pass')
        re_password = request.POST.get('txt_repassword')

        # Basic Password Validation
        if password == re_password:
            tbl_user.objects.create(user_name=name, user_email=email,user_contact=contact,user_address=address,user_gender=gender,user_dob=dob,place_id=place_id,user_photo=photo,user_password=password)
            return redirect("Guest:Login") # Replace with your success URL
        else:
            return render(request,"Guest/UserRegistration.html", {'msg': "Passwords do not match!"})
    else:
        return render(request,"Guest/UserRegistration.html", {'districtData': districts, 'placeData': places})
def Login(request):
    if request.method == 'POST':
       
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_pass')
        adminCount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        userCount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        if adminCount>0:
            adminData=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['aid']=adminData.id
            return redirect('Admin:admin_home')
        elif userCount>0:
            userData=tbl_user.objects.get(user_email=email,user_password=password)
            request.session['uid']=userData.id
            return redirect('User:Homepage') 
        else:
            return render(request,'Guest/Login.html',{'msg': "Invalid Email Or Password"})
    else:
          return render(request,'Guest/Login.html')


def ajaxplace(request):
    district_id=tbl_district.objects.get(id=request.GET.get("did"))
    place=tbl_place.objects.filter(district_id=district_id)
    return render(request,"Guest/AjaxPlace.html",{"place":place}) 


def Index(request):
    tbl_visit.objects.create()
    return render(request, "Guest/Index.html")

def ViewGallery(request):
    g_data=tbl_gallery.objects.all()
    return render(request,'Guest/ViewGallery.html',{'g_data':g_data})

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        user = tbl_user.objects.get(user_email=email)
        otp = random.randint(111111,999999)
        request.session["otp"] = otp
        request.session["fid"] = user.id
        send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/ForgotPassword.html",{"msg":email})
    else:
        return render(request,"Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))
        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Matches..!!"})
    else:
        return render(request,"Guest/OTP.html")

def newpass(request):
    if request.method == "POST":
        user = tbl_user.objects.get(id=request.session["fid"])
        if request.POST.get("txt_new_pass") == request.POST.get("txt_con_pass"):
            user.user_password = request.POST.get("txt_con_pass")
            user.save()
            return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
        else:
            return render(request,"Guest/NewPassword.html",{"msg":"Error in confirm password..!!!"})
    else:
        return render(request,"Guest/NewPassword.html")

def Festivals(request):
       return render(request,'Guest/Festivals.html')
def Shivan(request):
       return render(request,'Guest/Shivan.html')
def Kali(request):
       return render(request,'Guest/Kali.html')
def Nagam(request):
       return render(request,'Guest/Nagam.html')
def Kurup(request):
       return render(request,'Guest/Kurup.html')
def Chamundi(request):
       return render(request,'Guest/Chamundi.html')
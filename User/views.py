from django.shortcuts import render,redirect 
from Guest.models import *
from Admin.models import *
from User.models import *
import razorpay
from django.conf import settings
from django.utils import timezone
import random
# Create your views here.
def Myprofile(request):
    # Fetch user data using the session ID created during login
    u_data = tbl_user.objects.get(id=request.session['uid']) 
    return render(request,'User/Myprofile.html',{'userData': u_data})

def Editprofile(request):
    # 1. Always fetch the current user's record first
    # This uses the session 'uid' created at login
    user_id = request.session.get('uid')
    u_data = tbl_user.objects.get(id=user_id)

    if request.method == 'POST':
        # 2. Update the record with data from the form
        u_data.user_name = request.POST.get('txt_name') 
        u_data.user_email = request.POST.get('txt_email')
        u_data.user_contact = request.POST.get('txt_contact')
        u_data.user_address = request.POST.get('txt_address')
        
        # 3. Save changes to the database
        u_data.save()
        
        # Return the page with a success message
        return render(request, 'User/Myprofile.html', {
            'userData': u_data, 
            'msg': "Profile Updated Successfully!"
        })
    else:
        # 4. Display the page with existing data
        return render(request, 'User/Editprofile.html', {'userData': u_data})
    
def Changepassword(request):
    if request.method == 'POST':
        # 1. Identify the logged-in user
        user_id = request.session.get('uid')
        u_data = tbl_user.objects.get(id=user_id)
        
        # 2. Get data from the form
        old_pass = request.POST.get('txt_oldpass') 
        new_pass = request.POST.get('txt_newpass')
        re_pass = request.POST.get('txt_repass')

        # 3. Check if Old Password is correct
        if u_data.user_password == old_pass:
            
            # 4. Check if New Passwords match each other
            if new_pass == re_pass:
                # 5. Update and save
                u_data.user_password = new_pass
                u_data.save()
                msg = "Password Updated Successfully!"
                return render(request, 'User/MyProfile.html', {'msg': msg})
            else:
                msg = "New Password Mismatch!"
                return render(request, 'User/Changepassword.html', {'msg': msg})
        else:
            msg = "Old Password Incorrect!"
            return render(request, 'User/Changepassword.html', {'msg': msg})
    else:
        return render(request, 'User/Changepassword.html')

def Feedback(request):
    feeddata=tbl_feedback.objects.filter(user_id=request.session['uid'])
    if request.method=='POST':
        content=request.POST.get('txt_feedback')
        user=tbl_user.objects.get(id=request.session['uid'])
        tbl_feedback.objects.create(feedback_content=content,user_id=user)
        return render(request, 'User/Feedback.html', {'msg': "Feedback Added"})
    else:
        return render(request, 'User/Feedback.html', {'feeddata': feeddata})

def Homepage(request):
       return render(request,'User/Homepage.html')

def ViewGallery(request):
    g_data=tbl_gallery.objects.all()

    return render(request,'User/ViewGallery.html',{'g_data':g_data})


def Poojabooking(request):
    # Fetching data for the dropdowns
    u_data = tbl_user.objects.get(id=request.session['uid']) 
    pooja = tbl_pooja.objects.all()
    deity = tbl_deity.objects.all()
    birthstar = tbl_birthstar.objects.all()
    if request.method == "POST":
        # Capturing text and selection data
        name = request.POST.get('txt_name')
        number = request.POST.get('txt_number')
        date = request.POST.get('txt_date')
        deity=tbl_deity.objects.get(id=request.POST.get('sel_deity'))
        pooja=tbl_pooja.objects.get(id=request.POST.get('sel_pooja'))
        birthstar=tbl_birthstar.objects.get(id=request.POST.get('sel_birthstar'))
        tbl_booking.objects.create(booking_number=number,booking_todate=date,pooja_id=pooja,user_id=u_data)   
            
        return render(request,'User/Poojabooking.html',{'msg':"inserted"})
    else:
            return render(request,'User/Poojabooking.html',{'poojaData':pooja,'deityData':deity,'birthdata':birthstar,})

def ajaxpooja(request):
    deity=tbl_deity.objects.get(id=request.GET.get("did"))
    pooja=tbl_pooja.objects.filter(deity_id=deity)
    return render(request,"User/AjaxPooja.html",{"pooja":pooja}) 

def Mybooking(request):
    # Fetch all bookings for the logged-in user, excluding the active cart (status 0)
    bookingData = tbl_booking.objects.filter(
        user_id=request.session["uid"]
    ).exclude(
        booking_status=0
    ).order_by('-created_at') # Shows newest bookings first
    
    return render(request, 'User/MyBookings.html', {'bookingdata': bookingData})



def Payment(request, bid):
    bookingdata = tbl_booking.objects.get(id=bid)
    
    # Razorpay Client Setup (Replace with your actual keys or use settings)
    client = razorpay.Client(auth=("rzp_test_SUeshZUvuvztS6", "lioU9lyee1G4NyGWnEBOJU2v"))

    # Razorpay expects amount in paise (multiply by 100)
    amount_in_paise = int(bookingdata.booking_total) * 100 

    # Create Razorpay Order
    data = { "amount": amount_in_paise, "currency": "INR", "receipt": f"order_{bid}" }
    payment = client.order.create(data=data)
    
    context = {
        'bookingdata': bookingdata,
        'payment': payment, # This contains the order_id
        'razorpay_key_id': "rzp_test_SUeshZUvuvztS6",
        'amount_in_paise': amount_in_paise
    }

    if request.method == "POST":
        # Usually, you'd verify the signature here
        bookingdata.booking_status = 3
        bookingdata.save()
        return render(request, 'User/MyBookings.html', {'msg': "Payment Successful!"})

    return render(request, 'User/Payment.html', context)

def ViewPoojas(request):
    # 1. Fetch all active deities for the dropdown
    deities = tbl_deity.objects.filter(deity_is_active=True)
    
    # 2. Start with all poojas
    p_data = tbl_pooja.objects.all()

    # 3. Handle the search form submission
    if request.method == "POST":
        search_text = request.POST.get("txt_search")
        deity_val = request.POST.get("sel_deity")

        # Filter by Pooja Name if text was entered (icontains makes it case-insensitive)
        if search_text:
            p_data = p_data.filter(pooja_name__icontains=search_text)
            
        # Filter by Deity if one was selected from the dropdown
        if deity_val:
            p_data = p_data.filter(deity_id=deity_val)

    # 4. Pass the data back to the template
    return render(request, 'User/ViewPoojas.html', {
        'poojaData': p_data,
        'deities': deities
    })

def AddCart(request, pid):
    poojadata = tbl_pooja.objects.get(id=pid)
    userdata = tbl_user.objects.get(id=request.session["uid"])
    today = timezone.now().date()

    # Check for an active 'Pending' booking for this user
    bookingcount = tbl_booking.objects.filter(user_id=userdata, booking_status=0).count()
    
    if bookingcount > 0:
        bookingdata = tbl_booking.objects.get(user_id=userdata, booking_status=0)
        
        # Check if this specific pooja is already in the booking items
        itemcount = tbl_booking_item.objects.filter(booking_id=bookingdata, pooja_id=poojadata).count()
        if itemcount > 0:
            msg = "Pooja already added to booking"
            return render(request, "User/ViewPoojas.html", {'msg': msg})
        else:
            # Add new item to existing booking
            tbl_booking_item.objects.create(
                booking_id=bookingdata,
                pooja_id=poojadata,
                quantity=1,
                pooja_date=today, # Defaulting to today; you may want to let users select this later
                rate=poojadata.pooja_amount,
                line_total=poojadata.pooja_amount
            )
            msg = "Added to booking"
            return render(request, "User/ViewPoojas.html", {'msg': msg})
    else:
        # Create a new booking
        b_num = f"TEMPLE{timezone.now().year}{random.randint(10000, 99999)}"
        bookingdata = tbl_booking.objects.create(
            user_id=userdata,
            booking_number=b_num,
            booking_from_date=today
        )
        
        # Add item to the new booking
        tbl_booking_item.objects.create(
            booking_id=bookingdata,
            pooja_id=poojadata,
            quantity=1,
            pooja_date=today,
            rate=poojadata.pooja_amount,
            line_total=poojadata.pooja_amount
        )
        msg = "Added to booking"
        return render(request, "User/ViewPoojas.html", {'msg': msg})

def MyCart(request):
    if request.method == "POST":
        bookingdata = tbl_booking.objects.get(id=request.session["bookingid"])
        
        # Update overall booking details
        bookingdata.booking_total = request.POST.get("carttotalamt")
        bookingdata.booking_status = 1  # Confirmed status
        
        # --- NEW: Capture and save the Date Range ---
        from_date = request.POST.get("booking_from_date")
        to_date = request.POST.get("booking_to_date")
        
        if from_date:
            bookingdata.booking_from_date = from_date
            
        if to_date:
            bookingdata.booking_to_date = to_date
        else:
            # If they leave it blank, clear any existing to_date
            bookingdata.booking_to_date = None 
        # --------------------------------------------
        
        bookingdata.save()
        
        # Save devotee details and update status for EACH item
        items = tbl_booking_item.objects.filter(booking_id=bookingdata)
        for i in items:
            devotee_name = request.POST.get(f"devotee_name_{i.id}")
            birthstar_val = request.POST.get(f"birthstar_{i.id}")
            special_req = request.POST.get(f"special_request_{i.id}")

            i.devotee_name = devotee_name
            i.special_request = special_req
            
            if birthstar_val:
                i.birthstar_id = tbl_birthstar.objects.get(id=birthstar_val)
            else:
                i.birthstar_id = None
                
            i.item_status = 1
            i.save()
            
        return redirect("User:Payment",request.session["bookingid"])
        
    else:
        # ... your existing GET logic ...
        bookcount = tbl_booking.objects.filter(user_id=request.session["uid"], booking_status=0).count()
        if bookcount > 0:
            book = tbl_booking.objects.get(user_id=request.session["uid"], booking_status=0)
            request.session["bookingid"] = book.id
            
            items = tbl_booking_item.objects.filter(booking_id=book)
            birthstars = tbl_birthstar.objects.all() 
            
            return render(request, "User/MyCart.html", {
                'cartdata': items, 
                'birthstars': birthstars,
                'booking_obj': book  # Make sure this is still here!
            })
        else:
            return render(request, "User/MyCart.html")
        


   
def DelCart(request, did):
    tbl_booking_item.objects.get(id=did).delete()
    return redirect("User:MyCart")

def CartQty(request):
    qty = int(request.GET.get('QTY'))
    print(qty)
    itemid = request.GET.get('ALT')
    
    itemdata = tbl_booking_item.objects.get(id=itemid)
    itemdata.quantity = qty
    # Ensure line_total updates when quantity changes
    itemdata.line_total = itemdata.rate * qty 
    itemdata.save()
    
    return redirect("User:MyCart")

def Shivan(request):
       return render(request,'User/Shivan.html')
def Kali(request):
       return render(request,'User/Kali.html')
def Nagam(request):
       return render(request,'User/Nagam.html')
def Kurup(request):
       return render(request,'User/Kurup.html')
def Chamundi(request):
       return render(request,'User/Chamundi.html')
def Festivals(request):
       return render(request,'User/Festivals.html')
def History(request):
       return render(request,'User/History.html')
def Admin(request):
       return render(request,'User/Admin.html')
def Contact(request):
       return render(request,'User/Contact.html')

def logout(request):
    del request.session['uid']
    return redirect("Guest:Login")
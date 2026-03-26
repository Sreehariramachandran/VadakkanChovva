from django.shortcuts import render

# Create your views here.
def Sum(request):
    if request.method == "POST":
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        sum=a+b
        return render(request,'Basics/Sum.html',{'Result':sum})
    else:
        return render(request,'Basics/Sum.html')
def Largest(request):
    if request.method == "POST":
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        if a>b :
            largest = a
        else :
            largest=b
        return render(request,'Basics/Largest.html',{'Result':largest})
    else: 
        return render(request,'Basics/Largest.html')
def Calculator(request):
    if request.method == "POST":
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        op=request.POST.get('btn_submit')
        result = 0
        if op == "+":
            result=a+b
        elif op =="-":
            result=a-b
        elif op =="*":
            result=a*b
        elif op =="/" :
            result=a/b
        
        return render(request,'Basics/Calculator.html',{'Result':result})
    else: 
        return render(request,'Basics/Calculator.html')

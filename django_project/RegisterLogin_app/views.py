from django.template.defaulttags import csrf_token
from django.shortcuts import render
from django.http import HttpResponse
from .models import Register
from django.shortcuts import redirect
from django import forms
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
@csrf_exempt
def home(request):
    return render(request, 'RegisterLogin_app/home.html')


@csrf_exempt
def index(request):
    if 'register' in request.POST:
        print(request.POST)
        return render(request, 'RegisterLogin_app/registration.html')
    elif 'login' in request.POST:
        print(request.POST)
        return render(request, 'RegisterLogin_app/login.html')


# API for registration
@csrf_exempt      
def register_view(req):
    if req.method == "GET":
        return render(req, 'RegisterLogin_app/registration.html')
    else:
        name1 = req.POST.get("name")
        add = req.POST.get("address")
        mail = req.POST.get("email")
        passd = req.POST.get("password")
        con_pass = req.POST.get("confirm_pass")
        stat = req.POST.get("status")
        if passd != con_pass:
            return render(req, 'RegisterLogin_app/registration.html', {"message" : "Password and Confirm Password does't match!!"})
        if not Register.objects.filter(email=mail).exists():
            output = Register(name=name1, address=add, email=mail, password=passd, confirm_pass=con_pass, status=stat)
            output.save()
            return redirect('/login')
        else:
            return render(req, 'RegisterLogin_app/registration.html', {"message" : "Email already exists!!"})


# API for login
@login_required()
@csrf_exempt
def login_view(request):
    flag=0
    if request.method == "GET":
        return render(request,'RegisterLogin_app/login.html')
    else:        
        email = request.POST.get("email") or None
        password = request.POST.get("password") or None
        con_pass = request.POST.get("confirm_pass") or None
        if  Register.objects.filter(email=email, password=password, confirm_pass=con_pass).exists():
            info = Register.objects.get(email=email, password=password, confirm_pass=con_pass)
            content={
                "name":info.name,
                "address":info.address,
                "email":info.email,
                "status":info.status
            }
            if info.status == "HR":
                return redirect('/HR')
            elif info.status == "Employee":
                return redirect('/employee')
            else:
                return redirect('/cutomer')
        else:        
            return render(request,'RegisterLogin_app/login.html',{"message" : "Username or Password is wrong"})


# If role is HR then render to HR page
@login_required() # API required login to database
@csrf_exempt
def HR_view(req):
    print(req.user)
    qs = Register.objects.filter(status='HR')
    print(qs)
    context = {
        'query_list': qs
    }
    # Format of context is dictionary. Context are used to pass the value to the html page 
    return render(req,'RegisterLogin_app/HR.html', context)


# If role is employee then render to employee page
@csrf_exempt
def employee_view(req):
    qs = Register.objects.filter(status='Employee')
    print(qs)
    context = {
        'query_list': qs
    }
    return render(req,'RegisterLogin_app/employee.html', context)


# If role is customer then render to customer page
@csrf_exempt       
def customer_view(req):
    qs = Register.objects.filter(status='Customer')
    print(qs)
    context = {
        'query_list': qs
    }
    return render(req,'RegisterLogin_app/customer.html', context)


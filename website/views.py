from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AttendanceForm
from .models import Attendance
# Create your views here.
def home(request):
    return render(request, 'home.html',)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "Invalid credentials")
            return redirect('login')
        
    else:
        return render(request, 'login.html',)

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
    
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "you have Successfully Registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form':form})
    return render(request, 'register.html',{'form':form})

def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendanceList.html',{'attendances': attendances})

def time_In(request):
    form = AttendanceForm(request.POST or None)
    if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record Added")
                    return redirect('home')
            return render(request, 'timeIn.html',{'form':form})
    else:
        messages.success(request, "You Must be logged in to add record")
        return redirect('home')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AttendanceForm, TimeOutForm
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
    
def attendance_record(request, pk):
    if request.user.is_authenticated:
        attendance_record = Attendance.objects.get(id=pk)
        return render(request, 'attendanceRecord.html',{'attendance_record':attendance_record})
    else:
        messages.success(request, "You Must be logged in to view that page")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Attendance.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('attendanceList')
    else:
        messages.success(request, "You Must be logged in to delete this record")
        return redirect('attendanceList')
    
def time_Out(request, pk):
	if request.user.is_authenticated:
		current_record = Attendance.objects.get(id=pk)
		form = TimeOutForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('attendanceList')
		return render(request, 'timeOut.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('attendanceList')
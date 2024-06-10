from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  AttendanceForm, TimeOutForm, EditAttendanceFormAdmin, AttendanceFormAdmin, PayslipForm
from .models import Attendance
from django.urls import reverse
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
# Create your views here.

# landing page
def home(request):
    return render(request, 'home.html',)

def notfound(request):
    return render(request, '404.html',)
# login page (admin)
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect(reverse('welcome', kwargs={'username': username}))
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def welcome_view(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'welcome.html', {'username': username})
    else:
        logout(request)
        messages.success(request, "You must be logged it to access the page")
        return redirect('home')  
    
# logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


# attendance_list admin
def attendance_list(request, username):
    form = AttendanceFormAdmin(request.POST or None)
    if request.user.is_authenticated and request.user.username == username:
        if request.user.is_employee:
            employeeID = request.user.id
            attendances = Attendance.objects.filter(employeeID=employeeID)
        else:
            attendances = Attendance.objects.all()
            
        for attendance in attendances:
            time_difference = datetime.combine(datetime.today(), attendance.time_out) - datetime.combine(datetime.today(), attendance.time_in)
            hours = int(time_difference.total_seconds() / 3600)
            minutes = int((time_difference.total_seconds() % 3600) / 60)
            attendance.time_difference = f"{hours} hours {minutes} minutes"  # Formatting time_difference
            computed_salary = calculate_computed_salary(attendance.time_in, attendance.time_out, attendance.salary)
            attendance.computed_salary = computed_salary

        if request.user.is_superuser:
            if request.method == "POST" and form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added")
                return redirect('attendanceList', username=username)
            return render(request, 'attendanceList.html', {'form': form, 'attendances': attendances, 'username': username})
        return render(request, 'attendanceList.html', {'attendances': attendances, 'username': username})
    else:
        messages.success(request, "You must be logged in to view the attendance list")
        return redirect('home')

# create time in
def time_In(request, username):
    if request.user.is_authenticated and (request.user.username == username or request.user.is_superuser):
        today_records = Attendance.objects.filter(date=timezone.now().date(), employeeID=request.user.id)
        if today_records.exists():
            messages.error(request, "You have already timed in for today.")
            return redirect('attendanceList', username=username)

        if request.method == "POST":
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.user = request.user
                attendance.date = datetime.now().date()  # Set date to current date
                attendance.time_in = datetime.now().time()  # Set time_in to current time
                attendance.time_out = datetime.now().time()  # Set time_in to current time
                attendance.save()
                messages.success(request, "Record Added")
                return redirect('attendanceList', username=username)
        else:
            initial_data = {
                'employeeID': request.user.id,
                'employee_Name': f"{request.user.first_name} {request.user.last_name}",
                'date': datetime.now().date(),  # Set initial date to current date
                'time_in': datetime.now().time(),  # Set initial time_in to current time
            }
            form = AttendanceForm(initial=initial_data)
        return render(request, 'timeIn.html', {'form': form})
    else:
        return redirect('attendanceList', username=username)
    # time out
def time_Out(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        current_record = Attendance.objects.get(id=pk)
        truncated_time_in = truncate_to_minutes(current_record.time_in)
        truncated_time_out = truncate_to_minutes(current_record.time_out)
        current_time = datetime.now().time()
        if truncated_time_in == truncated_time_out:
            form = TimeOutForm(request.POST or None, instance=current_record)
            
            computed_salary = None
            working_hours = None
            if current_record.time_in and current_record.time_out:
                # Compute salary
                computed_salary = calculate_computed_salary_timeout(current_record.time_in, current_record.salary)
                
                # Compute work hours
                time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), current_record.time_in)
                hours = int(time_difference.total_seconds() / 3600)
                minutes = int((time_difference.total_seconds() % 3600) / 60)
                working_hours = f"{hours} hours {minutes} minutes"
            
            if computed_salary is not None:
                form.initial['salary_computation'] = computed_salary
            if working_hours is not None:
                form.initial['working_hours'] = working_hours
                
            # Set initial value for time_out to current time
            form.initial['time_out'] = current_time
            
            if form.is_valid():
                form.instance.on_duty = False
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('attendanceList', username=username)
            return render(request, 'timeOut.html', {'form': form, 'computed_salary': computed_salary, 'working_hours': working_hours})
        else:
            messages.warning(request, "Record already timed out.")
            return redirect('attendanceList', username=username)
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

 # admin attendance individual record
def attendance_record(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        attendance_record = Attendance.objects.get(id=pk)
        
        time_difference = datetime.combine(datetime.today(), attendance_record.time_out) - datetime.combine(datetime.today(), attendance_record.time_in)
        hours = int(time_difference.total_seconds() / 3600)
        minutes = int((time_difference.total_seconds() % 3600) / 60)
        formatted_time_difference = f"{hours} hours {minutes} minutes"  # Formatting time_difference
        
        computed_salary = calculate_computed_salary(attendance_record.time_in, attendance_record.time_out, attendance_record.salary)
        
        return render(request, 'attendanceRecord.html', {'attendance_record': attendance_record, 'computed_salary': computed_salary, 'formatted_time_difference': formatted_time_difference, 'username': username})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('home')


    # deletion of record
def delete_record(request, pk,username):
    if request.user.is_authenticated and request.user.username == username:
        delete_it = Attendance.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('attendanceList',  username=username)
    else:
        messages.success(request, "You Must be logged in to delete this record")
        return redirect('attendanceList', username=username)
# computations
def AdminUpdateAttendanceRecord(request, pk, username):
    if request.user.is_authenticated and request.user.username == username:
        if request.user.is_superuser:
            current_record = get_object_or_404(Attendance, pk=pk)
            if request.method == "POST":
                form = EditAttendanceFormAdmin(request.POST, instance=current_record)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Record has been updated successfully!")
                    return redirect('home')
            else:
                # Set initial values for time_in and time_out fields
                form = EditAttendanceFormAdmin(instance=current_record, initial={'time_in': current_record.time_in, 'time_out': current_record.time_out})
            return render(request, 'AdminEditAttendance.html', {'form': form, 'username': username})
        else:
            messages.error(request, "You must be an admin to edit this.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')
    
def create_payslip(request):
    form = PayslipForm(request.POST or None)
    if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_playslip = form.save()
                    messages.success(request, "Record Added")
                    return redirect('home')
            return render(request, 'create_payslip.html',{'form':form})
    else:
        messages.success(request, "You Must be logged in to add record")
        return redirect('home')





def truncate_to_minutes(time):
    return time.replace(second=0, microsecond=0)

def calculate_computed_salary(time_in, time_out, salary):
    time_difference = datetime.combine(datetime.today(), time_out) - datetime.combine(datetime.today(), time_in)
    hours_difference = time_difference.total_seconds() / 3600
    salary_decimal = Decimal(salary)
    computed_salary = (salary_decimal / Decimal(9)) * Decimal(hours_difference)
    computed_salary = computed_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return computed_salary

def calculate_computed_salary_timeout(time_in, salary):
    current_time = datetime.now().time()
    time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), time_in)
    hours_difference = time_difference.total_seconds() / 3600
    salary_decimal = Decimal(salary)
    computed_salary = (salary_decimal / Decimal(9)) * Decimal(hours_difference)
    computed_salary = computed_salary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return computed_salary





    


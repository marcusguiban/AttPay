from django.urls import path
from . import views
urlpatterns = [


    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('attendance/list/<str:username>', views.attendance_list, name='attendanceList'),
    path('attendance/time-in/<str:username>', views.time_In, name='time_In'),
    path('attendance/record/<str:username>/<int:pk>', views.attendance_record, name='attendance_record'),
    path('attendacen/delete/<str:username>/<int:pk>', views.delete_record, name='delete_record'),
    path('attendance/time-out/<str:username>/<int:pk>', views.time_Out, name='time_Out'),
    path('attendace/edit/<str:username>/<int:pk>', views.AdminUpdateAttendanceRecord, name='Edit_attendance'),
    path('notfound/', views.notfound, name='notfound'),
    path('payslip/<str:username>', views.create_payslip, name='payslip'),
    path('payslip/record/<str:username>', views.payslip_list, name='payslip_list'),
    path('payslip/record/<str:username>/<int:pk>', views.payslip_record, name='payslip_record'),
    path('payslip/delete/<str:username>/<int:pk>', views.delete_payslip, name='delete_payslip'),
    path('payslip/update/<str:username>/<int:pk>', views.update_payslip, name='update_payslip'),
    path('schedule/<str:username>', views.schedule_create, name='schedule_create'),
    path('schedule/list/<str:username>', views.schedule_list, name='schedule_list'),
    path('schedule/record/<str:username>/<int:pk>', views.schedule_record, name='schedule_record'),
    path('schedule/update/<str:username>/<int:pk>', views.schedule_update, name='schedule_update'),
    path('schedule/delete/<str:username>/<int:pk>', views.schedule_delete, name='schedule_delete'),
]

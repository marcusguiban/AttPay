from django.urls import path
from . import views
urlpatterns = [


    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('attendanceList/<str:username>', views.attendance_list, name='attendanceList'),
    path('TimeIn/<str:username>', views.time_In, name='time_In'),
    path('attendance_record/<str:username>/<int:pk>', views.attendance_record, name='attendance_record'),
    path('delete_record/<str:username>/<int:pk>', views.delete_record, name='delete_record'),
    path('TimeOut/<str:username>/<int:pk>', views.time_Out, name='time_Out'),
    path('welcome/<str:username>/', views.welcome_view, name='welcome'),
    path('notfound/', views.notfound, name='notfound'),


]

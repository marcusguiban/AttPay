from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('attendanceList/', views.attendance_list, name='attendanceList'),
    path('TimeIn/', views.time_In, name='time_In'),
    path('attendance_record/<int:pk>', views.attendance_record, name='attendance_record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('TimeOut/<int:pk>', views.time_Out, name='time_Out'),
    path('welcome/<str:username>/', views.welcome_view, name='welcome')
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
]
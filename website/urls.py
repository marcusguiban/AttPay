from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/', views.attendance_list, name='record'),

    path('TimeIn/', views.time_In, name='time_In'),
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
]
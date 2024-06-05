from django.urls import path
from . import views
urlpatterns = [


    # path('home/', views.home, name='home2'),
    path('supervisor_register/',views.supervisor_register.as_view(), name='supervisor_register'),
    path('employee_register/',views.employee_register.as_view(), name='employee_register'),
    # path('login/',views.login_request, name='login'),
    # path('logout/',views.logout_view, name='logout'),
]
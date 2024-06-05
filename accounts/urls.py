from django.urls import path
from . import views
urlpatterns = [



    path('supervisor_register/',views.supervisor_register.as_view(), name='supervisor_register'),
    path('employee_register/',views.employee_register.as_view(), name='employee_register'),
    path('employee_list/',views.employee_list, name='employee_list'),
    path('supervisor_list/',views.supervisor_list, name='supervisor_list'),

]
from django.urls import path
from . import views
urlpatterns = [
    path('supervisor_register/<str:username>/',views.supervisor_register.as_view(), name='supervisor_register'),
    path('employee_register/<str:username>/',views.employee_register.as_view(), name='employee_register'),
    path('employee_list/<str:username>',views.employee_list, name='employee_list'),
    path('supervisor_list/<str:username>',views.supervisor_list, name='supervisor_list'),
    path('employee_record/<str:username>/<int:pk>', views.employee_record, name='employee_record'),
    path('supervisor_record/<str:username>/<int:pk>', views.supervisor_record, name='supervisor_record'),
    path('employee_record/edit/<str:username>/<int:pk>', views.employee_update, name='employee_update'),
    path('supervisor_record/edit/<str:username>/<int:pk>', views.supervisor_update, name='supervisor_update'),
    path('delete_employee/<str:username>/<int:pk>', views.delete_employee, name='delete_employee'),
    path('delete_supervisor/<str:username>/<int:pk>', views.delete_supervisor, name='delete_supervisor'),
]
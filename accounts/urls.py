from django.urls import path
from . import views
urlpatterns = [



    path('supervisor_register/<str:username>/',views.supervisor_register.as_view(), name='supervisor_register'),
    path('employee_register/<str:username>/',views.employee_register.as_view(), name='employee_register'),
    path('employee_list/<str:username>',views.employee_list, name='employee_list'),
    path('supervisor_list/<str:username>',views.supervisor_list, name='supervisor_list'),
    # path('supervisor_list/',views.supervisor_list, name='supervisor_list'),   
    path('employee_record/<str:username>/<int:pk>', views.employee_record, name='employee_record'),
    path('supervisor_record/<str:username>/<int:pk>', views.supervisor_record, name='supervisor_record'),
    path('employee_record/edit/<str:username>/<int:pk>', views.employee_update, name='employee_update'),
]
from django.urls import path
from .views import rapport_pointage, person_list, add_person, edit_person, delete_person, detail_person, pointage_list, add_pointage, department_list, add_department, shift_list, add_shift, edit_shift, delete_shift, edit_department, delete_department

urlpatterns = [
    path('rapport_pointage/', rapport_pointage, name='rapport_pointage'),
    path('person_list/', person_list, name='person_list'),
    path('add_person/', add_person, name='add_person'),
    path('edit_person/<int:person_id>/', edit_person, name='edit_person'),
    path('delete_person/<int:person_id>/', delete_person, name='delete_person'),
    path('detail_person/<int:person_id>/', detail_person, name='detail_person'),
    path('Pointage/', pointage_list, name='pointage_list'),
    path('Pointage/add/', add_pointage, name='add_pointage'),
    path('departments/', department_list, name='department_list'),
    path('departments/add/', add_department, name='add_department'),
    path('edit_department/<int:department_id>/', edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', delete_department, name='delete_department'),
    path('shifts/', shift_list, name='shift_list'),
    path('shifts/add/', add_shift, name='add_shift'),
    path('edit_shift/<int:shift_id>/', edit_shift, name='edit_shift'),
    path('delete_shift/<int:shift_id>/', delete_shift, name='delete_shift'),
]

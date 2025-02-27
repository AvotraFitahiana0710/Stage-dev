from django.urls import path
from .views import dashboard_employe, login_employe, logout_employe, pointage_list_employe, add_pointage_employe

urlpatterns = [
    path('dashboard_employe', dashboard_employe, name='dashboard_employe'),
    path('login_employe/', login_employe, name='login_employe'),
    path('logout_employe/', logout_employe, name='logout_employe'),
    path('pointage_list_employe/', pointage_list_employe, name="pointage_list_employe"),
    path('add_pointage_employe/', add_pointage_employe, name="add_pointage_employe")
]
from django.urls import path
from .views import dashboard_admin, setup_admin, create_admin, login_admin, logout_admin, create_user

urlpatterns = [
    path('setup_admin', setup_admin, name='setup_admin'),
    path('login_admin/', login_admin, name='login_admin'),
    path('logout_admin/', logout_admin, name='logout_admin'),
    path('create_admin/', create_admin, name='create_admin'),
    path('dashboard_admin/', dashboard_admin, name='dashboard_admin'),
    path('create_user/', create_user, name='create_user'),
]
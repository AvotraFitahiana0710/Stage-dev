from django.urls import path
from .views import dashboard_user, login_user, logout_user

urlpatterns = [
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('dashboard_user/', dashboard_user, name='dashboard_user'),
]

from django.urls import path
from .views import dashboard_admin, setup_admin, create_admin, login_admin, logout_admin, create_user, rapport_pointage, person_list, add_person, edit_person, delete_person, detail_person, pointage_list, add_pointage, department_list, add_department, edit_department, delete_department, shift_list, add_shift, edit_shift, delete_shift
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('setup_admin', setup_admin, name='setup_admin'),
    path('login_admin/', login_admin, name='login_admin'),
    path('logout_admin/', logout_admin, name='logout_admin'),
    path('create_admin/', create_admin, name='create_admin'),
    path('dashboard_admin/', dashboard_admin, name='dashboard_admin'),
    path('create_user/', create_user, name='create_user'),
    #Concernant les employés
    path('administrateur_rapport_pointage/', rapport_pointage, name='administrateur_rapport_pointage'),
    path('administrateur_person_list/', person_list, name='administrateur_person_list'),
    path('administrateur_add_person/', add_person, name='administrateur_add_person'),
    path('administrateur_edit_person/<int:person_id>/', edit_person, name='administrateur_edit_person'),
    path('administrateur_delete_person/<int:person_id>/', delete_person, name='administrateur_delete_person'),
    path('administrateur_detail_person/<int:person_id>/', detail_person, name='administrateur_detail_person'),
    path('administrateur_Pointage/', pointage_list, name='administrateur_pointage_list'),
    path('administrateur_Pointage/add/', add_pointage, name='administrateur_add_pointage'),
    path('administrateur_departments/', department_list, name='administrateur_department_list'),
    path('administrateur_departments/add/', add_department, name='administrateur_add_department'),
    path('administrateur_edit_department/<int:department_id>/', edit_department, name='administrateur_edit_department'),
    path('administrateur_delete_department/<int:department_id>/', delete_department, name='administrateur_delete_department'),
    path('administrateur_shifts/', shift_list, name='administrateur_shift_list'),
    path('administrateur_shifts/add/', add_shift, name='administrateur_add_shift'),
    path('administrateur_edit_shift/<int:shift_id>/', edit_shift, name='administrateur_edit_shift'),
    path('administrateur_delete_shift/<int:shift_id>/', delete_shift, name='administrateur_delete_shift'),
    # concernant le mot de passe oublié
    # Formulaire pour demander la réinitialisation du mot de passe
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),

    # Message de confirmation après l'envoi de l'e-mail
    path('mot-de-passe-oublie/confirme/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),

    # Page pour saisir un nouveau mot de passe (lien envoyé par e-mail)
    path('mot-de-passe-reinitialisation/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),

    # Page de confirmation finale après changement de mot de passe
    path('mot-de-passe-reinitialisation/complet/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

]
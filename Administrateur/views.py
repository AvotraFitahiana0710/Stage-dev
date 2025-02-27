from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import  UserAccount, Person, Departement
from .forms import UserAccountCreationForm, UserAccountLoginForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from django.utils.timezone import now


User = get_user_model()

# Create your views here.
def setup_admin(request):
    # Vérifier s'il existe un administrateur actif
    if UserAccount.objects.filter(is_admin=True, is_active=True).exists():
        return redirect('dashboard_admin')  # Redirige vers la page de connexion

    # Formulaire de création de compte pour l'administrateur
    if request.method == 'POST':
        form = UserAccountLoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user) # Connexion automatique après la création du compte
            return redirect('dashboard_admin')
    else:
        form = UserAccountLoginForm()

    return render(request, 'Administrateur/setup_admin.html', {'form': form})

def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                # Utiliser la méthode create_superuser
                admin_user = UserAccount.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password1,
                    role="Admin"
                )
                #login(request, admin_user)
                return redirect('login_admin')  # Redirigez après la création
            except Exception as e:
                return render(request, 'Administrateur/create_admin.html', {'error': str(e)})
        else:
            message = "Vérifier votre mot de passe"
    else:
        message = ""
    return render(request, 'Administrateur/create_admin.html', {'message' : message})


# Version 1
@csrf_protect
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        Admin = authenticate(request, username=username, password=password)
        
        if Admin is not None and Admin.is_staff:  # Vérifie que c'est bien un admin
            active_sessions = set(request.session.get('active_users', []))  # Convertit en set
            active_sessions.add(Admin.username)  # Ajoute l'utilisateur connecté
            request.session['active_users'] = list(active_sessions)  # Sauvegarde la session
            login(request, Admin)
            request.session.save()
            return redirect('dashboard_admin')
        else:
            message = "Nom d'utilisateur ou mot de passe incorrecte"    
    else:
        message = ""

    return render(request, 'Administrateur/login_admin.html', {'message' : message})
# Fin version 1





@login_required
def dashboard_admin(request):
    User = get_user_model()
    nbr_persons = Person.objects.count()  # Récupère toutes les données de la base
    nbr_department = Departement.objects.count()
    nbr_account = UserAccount.objects.count()

    nbr_admins = UserAccount.objects.filter(role="Admin").count()
    nbr_managers = UserAccount.objects.filter(role="Manager").count()
    nbr_employees = UserAccount.objects.filter(role="Employe").count()


    active_sessions = request.session.get('active_users', set())  # Récupérer les sessions actives
    request.session['active_users'] = list(active_sessions)
    # Nombre d'utilisateurs connectés
    connected_users = len(active_sessions)

    return render(request, 'Administrateur/dashboard_admin.html', {
        'nbr_persons': nbr_persons,
        'nbr_department' : nbr_department,
        'nbr_account' : nbr_account,
        'nbr_admins': nbr_admins,
        'nbr_managers': nbr_managers,
        'nbr_employees': nbr_employees,
        'list_active' : active_sessions,
        'connected_users': connected_users
        # 'nbr_user_connected': nbr_user_connected,
        })



# def logout_admin(request):
#     auth_logout(request)  # Supprime toutes les sessions de l'utilisateur
#     return redirect('index')

def logout_admin(request):
    active_sessions = request.session.get('active_users', set())
    
    # Supprimer l'utilisateur des sessions actives
    if request.user.username in active_sessions:
        active_sessions.remove(request.user.username)
        request.session['active_users'] = list(active_sessions)

    logout(request)
    return redirect('index')  # Rediriger vers la page de connexion


#Création et connexion des comptes utilisateurs
def create_user(request):
    if request.method == 'POST':
        form = UserAccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte utilisateur créé avec succès.")
            return redirect('create_user')
        else: 
            messages.error(request, "Veuilliez rééssayer")
    else:
        form = UserAccountCreationForm()
        # messages.error(request, "Utilisateur introuvable.")

    return render(request, 'Administrateur/create_user.html', {'form': form})

 

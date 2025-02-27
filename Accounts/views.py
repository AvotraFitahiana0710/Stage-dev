from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Administrateur.models import UserAccount
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth import logout as auth_logout

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from django.views.decorators.csrf import csrf_protect
from Administrateur.models import UserAccount, Person, Departement
from datetime import datetime, timedelta, date

# def some_view(request):
#     active_users = UserAccount.objects.filter(is_active=True)
#     return render(request, 'active_users.html', {'users': active_users})

# def user_status(request):
#     user = request.user
#     if hasattr(user, 'user_account') and user.user_account.is_active:
#         status = "Actif"
#     else:
#         status = "Inactif"
#     return render(request, 'user_status.html', {'status': status})


# def login_user(request):
#     if request.method == 'POST':
#         # username = form.cleaned_data['username']
#         # password = form.cleaned_data['password']
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         try:
#             # user = UserAccount.objects.get(username=username)
#             user = authenticate(request, username=username, password=password)
#             # if check_password(password, user.password):
#             if user:
#                 # request.session['user_id'] = user.id
#                 # request.session['user_role'] = user.role
# 				login(request, user)
                
#                 return redirect('dashboard_user')
#             else:
#                 message = "Mot de passe incorrect."
#         except UserAccount.DoesNotExist:
#             message = "Nom d'utilisateur introuvable."
#     else:
#         message = ""

#     return render(request, 'Accounts/login_user.html', {'message' : message})


# def login_user(request):
#     message = ""
#     if request.method == 'POST':
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         # Authentification de l'utilisateur
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)  # Connecte l'utilisateur
#             return redirect('dashboard_user')  # Redirige vers le tableau de bord
#         else:
#             message = "Nom d'utilisateur ou mot de passe incorrect."

#     return render(request, 'Accounts/login_user.html', {'message': message})

@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            active_sessions = set(request.session.get('active_users', []))  # Convertit en set
            active_sessions.add(user.username)  # Ajoute l'utilisateur connecté
            request.session['active_users'] = list(active_sessions)  # Sauvegarde la session
            login(request, user)
            if user.role == 'Manager':
                request.session.save()
                return redirect("dashboard_user")
            else:
                message = 'Ce compte n\'appartient pas à un manager'         
        else:
            message = "Nom d'utilisateur ou mot de passe incorrect."
    else:
        message = ""

    return render(request, 'Accounts/login_user.html', {'message' : message})

# def logout_user(request):
#     logout(request)
#     return redirect('login_user')  # Redirige vers la page de connexion

@login_required(login_url="/login_user/")
def dashboard_user(request):
    user = request.user  # L'utilisateur connecté actuel
    nbr_persons = Person.objects.count()  # Récupère toutes les données de la base
    nbr_department = Departement.objects.count()

    if user.is_authenticated:  # Vérifie si l'utilisateur est authentifié
        return render(request, 'Accounts/dashboard_user.html', 
            {
                'user': user, 'nbr_persons': nbr_persons,
                'nbr_department' : nbr_department,
            })
    else:
        return redirect('login_user')

def logout_user(request):
    # active_sessions = request.session.get('active_users', set())
    
    # # Supprimer l'utilisateur des sessions actives
    # if request.user.username in active_sessions:
    #     active_sessions.remove(request.user.username)
    #     request.session['active_users'] = list(active_sessions)

    # logout(request)
    # username = request.user.username  # Récupérer l'utilisateur avant de logout
    # # return redirect('index')  # Rediriger vers la page de connexion
    # active_sessions = set(request.session.get('active_users', []))  
    # active_sessions.discard(username)  # Supprime l'utilisateur s'il existe
    # request.session['active_users'] = list(active_sessions)
    # return redirect('index')

    username = request.user.username  # Récupérer l'utilisateur avant de logout
    active_sessions = set(request.session.get('active_users', []))  
    active_sessions.discard(username)  # Supprime l'utilisateur s'il existe
    request.session['active_users'] = list(active_sessions)
    session_key = f"session_user_{request.user.id}"
    if session_key in request.session:
        del request.session[session_key]

    logout(request)
    return redirect('index')
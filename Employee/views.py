from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Administrateur.models import UserAccount
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth import logout as auth_logout
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from Administrateur.models import UserAccount, Person, Departement
from Manager.models import Pointage
from django.views.decorators.csrf import csrf_protect
from django.utils.timezone import now
from django.contrib import messages
from Manager.forms import PointageForm
from datetime import datetime, timedelta, date
import calendar



User = get_user_model()
@csrf_protect
def login_employe(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            active_sessions = set(request.session.get('active_users', []))  # Convertit en set
            active_sessions.add(user.username)  # Ajoute l'utilisateur connecté
            request.session['active_users'] = list(active_sessions)  # Sauvegarde la session
            login(request, user)
            request.session.save()
            if user.role == "Employee":  
                request.session.save()  
                return redirect("dashboard_employe")
            else:
                messages.error(request, 'Ce compte n\'appartient pas à un employé')
            
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'Employee/login_employe.html')

@login_required(login_url="/login_user/")
def dashboard_employe(request):
    user = request.user  # L'utilisateur connecté actuel
    mois_en_cours = now().month
    annee_en_cours = now().year

    # Convertir le numéro du mois en son nom (ex: 2 -> "Février")
    mois_nom = calendar.month_name[mois_en_cours]  # En anglais ("February")
    mois_nom_fr = calendar.month_name[mois_en_cours].capitalize()  # Pour mettre la première lettre en majuscule
    
    active_sessions = set(request.session.get('active_users', []))  # Convertit en set
    active_sessions.add(user.username)  # Ajoute l'utilisateur connecté
    request.session['active_users'] = list(active_sessions)  # Sauvegarde la session
    request.session.save()        
    return render(request, 'Employee/dashboard_employe.html', {
        'user': user,
        # 'retards': retards,
        # 'conges': conges,
        # 'mois_en_cours' : mois_nom_fr,
        # 'annee_en_cours' : annee_en_cours
    })


def logout_employe(request):
    username = request.user.username
    active_sessions = set(request.session.get('active_users', []))  
    active_sessions.discard(username)  # Supprime l'utilisateur s'il existe
    request.session['active_users'] = list(active_sessions)
    logout(request)
    return redirect('index')

# def enregistrer_pointage(request):
#     utilisateur = request.user
#     date_aujourd_hui = now().date()
#     heure_actuelle = now().time()
#     message = ""
#     # Vérifier si l'utilisateur a déjà pointé aujourd'hui
#     if not Pointage.objects.filter(utilisateur=utilisateur, date_pointage=date_aujourd_hui).exists():
#         # Définir une heure d'arrivée standard (ex: 08:00)
#         heure_standard = timedelta(hours=8)
#         heure_arrivee = timedelta(hours=heure_actuelle.hour, minutes=heure_actuelle.minute)
#         est_retard = heure_arrivee > heure_standard  # Détermine si l'utilisateur est en retard

#         Pointage.objects.create(utilisateur=utilisateur, est_retard=est_retard)
#     else:
#         message = "Le pointage est déjà effectué pour aujourd'hui"
#     return redirect('dashboard_employe')

def add_pointage_employe(request):
    # utilisateur = request.user
    # # if not hasattr(utilisateur, 'employee'):
    # #     messages.error(request, "Votre compte n'est pas associé à un employé.")
    # #     return redirect('pointage_list_employe')
    # personne = getattr(utilisateur, 'employee', None)  # Utilisation de getattr pour éviter les erreurs
    # if personne is None:
    #     messages.error(request, "Votre compte n'est pas associé à un employé.")
    #     return redirect('pointage_list_employe')
    # if request.method == 'POST':
    #     form = PointageForm(request.POST)
    #     if form.is_valid():
    #         person = utilisateur.employee
    #         date_pointage = now().date()  # Ajout automatique de la date
    #         if Pointage.objects.filter(person=person, date_pointage=date_pointage).exists():
    #             messages.error(request, "Cet employé a déjà un pointage pour aujourd'hui.")
    #             return redirect('add_pointage_employe')

    #         pointage = form.save(commit=False)
    #         pointage.person = person
    #         pointage.date_pointage = date_pointage
    #         pointage.save()
    #         messages.success(request, 'Ajout réussi.')
    #         return redirect('pointage_list_employe')

    # else:
    #     form = PointageForm()
    # return render(request, 'Employee/formulaire_pointage_employe.html', {'form': form})
    utilisateur = request.user
    personne = getattr(utilisateur, 'employee', None)  # Vérifier si l'utilisateur est un employé

    if personne is None:
        messages.error(request, "Votre compte n'est pas associé à un employé.")
        return redirect('pointage_list_employe')

    date_pointage = now().date()
    pointage, created = Pointage.objects.get_or_create(
        person=personne, 
        date_pointage=date_pointage,
        defaults={'check_in': now().time()}  # Si c'est le premier pointage du jour, enregistre l'heure d'arrivée
    )

    if not created:  # Si l'enregistrement existe déjà (check-in fait), on enregistre l'heure de départ
        if pointage.check_out is None:
            pointage.check_out = now().time()
            pointage.save()
            messages.success(request, "Heure de départ enregistrée avec succès.")
        else:
            messages.error(request, "Vous avez déjà enregistré votre heure d'arrivée et de départ aujourd'hui.")
    else:
        messages.success(request, "Heure d'arrivée enregistrée avec succès.")

    return redirect('pointage_list_employe')  # Redirige après chaque action

def pointage_list_employe(request):
    
    # Récupérer les paramètres de tri
    utilisateur = request.user
    employee_id = request.user.id
    period = request.GET.get('period')  # 'week', 'month', ou 'day'
    selected_date = request.GET.get('date')  # Pour le tri par jour
    start_date = request.GET.get('start_date')  # Date de début
    end_date = request.GET.get('end_date')  # Date de fin
    person = utilisateur.employee

    # Récupérer la liste initiale des pointages
    records = Pointage.objects.filter(person=person).order_by('-date_pointage')

    # Filtrer par période (semaine, mois ou jour)
    if period == 'week':
        start_date = now() - timedelta(days=now().weekday())
        end_date = now().date()
        records = records.filter(date_pointage__gte=start_date)
    elif period == 'month':
        start_date = now().replace(day=1)
        end_date = now().date()
        records = records.filter(date_pointage__gte=start_date)
    elif period == 'day' and selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            records = records.filter(date_pointage=selected_date_obj)
        except ValueError:
            pass  # Si la date est invalide, ne filtre pas
    elif period =='custom':
    # Filtrer par date de début et de fin
        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                records = records.filter(date_pointage__range=[start_date_obj, end_date_obj])
            except ValueError:
                pass  # Si les dates sont invalides, ne filtre pas
    else:
        pass
    # Passer les employés et départements pour le formulaire de tri
    return render(request, 'Employee/pointage_employe.html', {
        'records': records,
        'selected_period': period,
        'selected_date': selected_date,
        'start_date': start_date,
        'end_date': end_date,
    })

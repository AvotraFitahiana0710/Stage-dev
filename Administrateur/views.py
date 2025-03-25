from django.shortcuts import render, redirect, get_object_or_404
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
from django.utils.timezone import now, timezone
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField, Q, Case, When
from Manager.models import Pointage, Shift
from Manager.forms import PersonForm, PointageForm, DepartmentForm, ShiftForm

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
                messages.success(request, "Compte créé avec succès")
                #login(request, admin_user)
                return redirect('login_admin')  # Redirigez après la création
            except Exception as e:
                return render(request, 'Administrateur/create_admin.html', {'error': str(e)})
        else:
            messages.error(request, "veuillez reéssayer")

    return render(request, 'Administrateur/create_admin.html')


# Version 1
@csrf_protect
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        Admin = authenticate(request, username=username, password=password)
        if Admin.role != "Admin":
            messages.error(request, "L'utilisateur n'est pas administrateur")
            return redirect('login_admin')
        if Admin is not None and Admin.is_staff:  # Vérifie que c'est bien un admin
            active_sessions = set(request.session.get('active_users', []))  # Convertit en set
            active_sessions.add(Admin.username)  # Ajoute l'utilisateur connecté
            request.session['active_users'] = list(active_sessions)  # Sauvegarde la session
            login(request, Admin)
            request.session.save()
            return redirect('dashboard_admin')
        else:
            # message = "Nom d'utilisateur ou mot de passe incorrecte"
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrecte")    

    return render(request, 'Administrateur/login_admin.html')
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
    request.session.save()
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

 
#Concernant les employés

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde dans la base de données
            return redirect('administrateur_person_list')  # Redirige vers la liste des personnes
    else:
        form = PersonForm()
    return render(request, 'Administrateur/add_person.html', {'form': form})

def person_list(request):
    user = request.user
    persons = Person.objects.all()  # Récupère toutes les données de la base
    return render(request, 'Administrateur/Person_List.html', {'persons': persons})

def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('administrateur_person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'Administrateur/edit_person.html', {'form': form, 'person': person})

def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        person.delete()  # Supprime la personne de la base de données
        return redirect('administrateur_person_list')
    return render(request, 'Administrateur/delete_person.html', {'person': person})

def detail_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        first_name = first_name.POST
        last_name = last_name.POST
        phone_number = phone_number.POST
    else:
        form = PersonForm(instance=person)
    return render(request, 'Administrateur/detail_person.html', {'form': form, 'person': person})


#concernant le pointage

def pointage_list(request):
    # Récupérer les paramètres de tri
    utilisateur = request.user
    # employee_id = request.user.id
    period = request.GET.get('period')  # 'week', 'month', ou 'day'
    selected_date = request.GET.get('date')  # Pour le tri par jour
    start_date = request.GET.get('start_date')  # Date de début
    end_date = request.GET.get('end_date')  # Date de fin

    # Récupérer la liste initiale des pointages
    # records = Pointage.objects.filter(person=person).order_by('-date_pointage')
    records = Pointage.objects.all()
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
    return render(request, 'Administrateur/pointage_list.html', {
        'records': records,
        # 'selected_employee': employee_id,
        # 'selected_department': department_id,
        'selected_period': period,
        'selected_date': selected_date,
        'start_date': start_date,
        'end_date': end_date,
    })


def add_pointage(request):
    # if request.method == 'POST':
    #     form = PointageForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('pointage_list')
    # else:
    #     form = PointageForm()
    utilisateur = request.user
    if not hasattr(utilisateur, 'person'):
        messages.error(request, "Votre compte n'est pas associé à un employé.")
        return redirect('administrateur_pointage_list')
    if request.method == 'POST':
        form = PointageForm(request.POST)
        if form.is_valid():
            person = utilisateur.employee
            date_pointage = now().date()  # Ajout automatique de la date
            if Pointage.objects.filter(person=person, date_pointage=date_pointage).exists():
                messages.error(request, "Cet employé a déjà un pointage pour aujourd'hui.")
                return redirect('administrateur_add_pointage')

            pointage = form.save(commit=False)
            pointage.person = person
            pointage.date_pointage = date_pointage
            pointage.save()
            messages.success(request, 'Ajout réussi.')
            return redirect('administrateur_pointage_list')

    else:
        form = PointageForm()
    return render(request, 'Administrateur/pointage_form.html', {'form': form})
 
def department_list(request):
    departments = Departement.objects.all()
    return render(request, 'Administrateur/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrateur_department_list')
    else:
        form = DepartmentForm()
    return render(request, 'Administrateur/department_form.html', {'form': form})

def edit_department(request, department_id):
    department = get_object_or_404(Departement, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('administrateur_department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'Administrateur/edit_department.html', {'form': form, 'department': department})

def delete_department(request, department_id):
    department = get_object_or_404(Departement, id=department_id)
    if request.method == 'POST':
        department.delete()  # Supprime la personne de la base de données
        return redirect('administrateur_department_list')
    return render(request, 'Manager/delete_department.html', {'department': department})


# Gestion des shifts
def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'Administrateur/shift_list.html', {'shifts': shifts})

def add_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administrateur_shift_list')
    else:
        form = ShiftForm()
    return render(request, 'Administrateur/shift_form.html', {'form': form})

def edit_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('administrateur_shift_list')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'Manager/edit_shift.html', {'form': form, 'shift': shift})

def delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        shift.delete()  # Supprime la shift de la base de données
        return redirect('administrateur_shift_list')
    return render(request, 'Administrateur/delete_shift.html', {'shift': shift})



def rapport_pointage(request):
    report_type = request.GET.get('type', 'weekly')  # 'weekly' ou 'monthly'
    
    if report_type == 'weekly':
        start_date = now().date() - timedelta(days=7)
        end_date = now().date()
        overtime_threshold = 40  # Seuil d'heures avant les heures supplémentaires (hebdomadaire)
    elif report_type == 'monthly':
        start_date = now().date().replace(day=1)
        end_date = now().date()
        overtime_threshold = 160  # Seuil d'heures avant les heures supplémentaires (mensuel)
    elif report_type == 'custom':
        # Lire les dates depuis les paramètres GET
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if not start_date or not end_date:
                raise ValueError("Les dates de début et de fin doivent être fournies pour un rapport personnalisé.")
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            overtime_threshold = 160  # Valeur par défaut pour un triage personnalisé
        except ValueError as e:
            return render(request, 'Administrateur/rapport_pointage.html', {'error': str(e)})
    else:
        return render(request, 'Administrateur/rapport_pointage.html', {'error': 'Type de rapport invalide.'})


    # end_date = now().date()

    # Filtrer les pointages entre les dates spécifiées
    pointages = Pointage.objects.filter(date_pointage__range=[start_date, end_date])

    # Calculer la durée de travail pour chaque pointage
    pointages = pointages.annotate(
        duration=ExpressionWrapper(
            F('check_out') - F('check_in'),
            output_field=DurationField()
        )
    )

    # Regrouper par personne
    grouped_data = (
        pointages
        .values('person__first_name')  # Regrouper par nom d'utilisateur de l'employé
        .annotate(
            total_days=Count('id'),  # Compte les jours pointés
            total_days_worked=Count('id') - Count(Case(When(status='Absent', then=1))),  # Jours réellement travaillés
            total_hours=Sum('hours_worked'),  # Total des heures travaillées
            total_absences=Count('id', filter=Q(status='Absent')),  # Total des absences
            total_conge=Count('id', filter=Q(status='Cong')),  # Total des jours de congé
            total_late=Count('id', filter=Q(status='Late'))  # Total des retards
        )
    )

    # Calculer les heures supplémentaires par employé en fonction du triage
    data_with_overtime = []
    for entry in grouped_data:
        total_hours = entry.get('total_hours', 0) or 0  # Évite les valeurs None
        overtime = max(0, total_hours - overtime_threshold)  # Heures sup = Heures travaillées - seuil
        entry['overtime_hours'] = overtime
        data_with_overtime.append(entry)

    return render(request, 'Administrateur/rapport_pointage.html', {
        'report_type': report_type,
        'grouped_data': data_with_overtime,
        'start_date': start_date,
        'end_date': end_date,
    })
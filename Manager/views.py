from django.shortcuts import render, redirect, get_object_or_404
from Administrateur.models import Person, Departement
from .models import Shift, Pointage
from django.http import HttpResponse
from datetime import datetime, timedelta, date
from django.utils.timezone import now, timezone
from .forms import PersonForm, PointageForm, DepartmentForm, ShiftForm
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField, Q, Case, When
from django.contrib import messages
# Create your views here.
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde dans la base de données
            return redirect('person_list')  # Redirige vers la liste des personnes
    else:
        form = PersonForm()
    return render(request, 'Manager/add_person.html', {'form': form})

def person_list(request):
    user = request.user
    persons = Person.objects.all()  # Récupère toutes les données de la base
    return render(request, 'Manager/Person_List.html', {'persons': persons})

def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'Manager/edit_person.html', {'form': form, 'person': person})

def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        person.delete()  # Supprime la personne de la base de données
        return redirect('person_list')
    return render(request, 'Manager/delete_person.html', {'person': person})

def detail_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        first_name = first_name.POST
        last_name = last_name.POST
        phone_number = phone_number.POST
    else:
        form = PersonForm(instance=person)
    return render(request, 'Manager/detail_person.html', {'form': form, 'person': person})


#concernant le pointage

def pointage_list(request):
    
    # # Récupérer les paramètres de tri
    # employee_id = request.GET.get('employee')
    # department_id = request.GET.get('department')
    # period = request.GET.get('period')  # 'week', 'month', ou 'day'
    # selected_date = request.GET.get('date')  # Pour le tri par jour
    # start_date = request.GET.get('start_date')  # Date de début
    # end_date = request.GET.get('end_date')  # Date de fin


    # # Récupérer la liste initiale des pointages
    # records = Pointage.objects.all()

    # # Filtrer par employé
    # if employee_id:
    #     records = records.filter(person_id=employee_id)

    # # Filtrer par département
    # if department_id:
    #     records = records.filter(person__department_id=department_id)

    # # Filtrer par période (semaine, mois ou jour)
    # if period == 'week':
    #     start_date = now() - timedelta(days=now().weekday())
    #     end_date = now().date()
    #     records = records.filter(date_pointage__gte=start_date)
    # elif period == 'month':
    #     start_date = now().replace(day=1)
    #     end_date = now().date()
    #     records = records.filter(date_pointage__gte=start_date)
    # elif period == 'day' and selected_date:
    #     try:
    #         selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    #         records = records.filter(date_pointage=selected_date_obj)
    #     except ValueError:
    #         pass  # Si la date est invalide, ne filtre pas
    # elif period =='custom':
    # # Filtrer par date de début et de fin
    #     if start_date and end_date:
    #         try:
    #             start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    #             end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    #             records = records.filter(date_pointage__range=[start_date_obj, end_date_obj])
    #         except ValueError:
    #             pass  # Si les dates sont invalides, ne filtre pas
    # else:
    #     pass
    # # Passer les employés et départements pour le formulaire de tri
    # employees = Person.objects.all()
    # departments = Departement.objects.all()

    # return render(request, 'Manager/pointage_list.html', {
    #     'records': records,
    #     'employees': employees,
    #     'departments': departments,
    #     'selected_employee': employee_id,
    #     'selected_department': department_id,
    #     'selected_period': period,
    #     'selected_date': selected_date,
    #     'start_date': start_date,
    #     'end_date': end_date,
    # })

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
        # 'records': records,
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
        return redirect('pointage_list')
    if request.method == 'POST':
        form = PointageForm(request.POST)
        if form.is_valid():
            person = utilisateur.employee
            date_pointage = now().date()  # Ajout automatique de la date
            if Pointage.objects.filter(person=person, date_pointage=date_pointage).exists():
                messages.error(request, "Cet employé a déjà un pointage pour aujourd'hui.")
                return redirect('add_pointage')

            pointage = form.save(commit=False)
            pointage.person = person
            pointage.date_pointage = date_pointage
            pointage.save()
            messages.success(request, 'Ajout réussi.')
            return redirect('pointage_list')

    else:
        form = PointageForm()
    return render(request, 'Manager/pointage_form.html', {'form': form})
 
def department_list(request):
    departments = Departement.objects.all()
    return render(request, 'Manager/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'Manager/department_form.html', {'form': form})

def edit_department(request, department_id):
    department = get_object_or_404(Departement, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'Manager/edit_department.html', {'form': form, 'department': department})

def delete_department(request, department_id):
    department = get_object_or_404(Departement, id=department_id)
    if request.method == 'POST':
        department.delete()  # Supprime la personne de la base de données
        return redirect('department_list')
    return render(request, 'Manager/delete_department.html', {'department': department})


# Gestion des shifts
def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'Manager/shift_list.html', {'shifts': shifts})

def add_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shift_list')
    else:
        form = ShiftForm()
    return render(request, 'Manager/shift_form.html', {'form': form})

def edit_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()  # Met à jour les données dans la base
            return redirect('shift_list')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'Manager/edit_shift.html', {'form': form, 'shift': shift})

def delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    if request.method == 'POST':
        shift.delete()  # Supprime la shift de la base de données
        return redirect('shift_list')
    return render(request, 'Manager/delete_shift.html', {'shift': shift})



def rapport_pointage(request):
    report_type = request.GET.get('type', 'weekly')  # 'weekly' ou 'monthly'
    
    if report_type == 'weekly':
        start_date = now().date() - timedelta(days=7)
        end_date = now().date()
    elif report_type == 'monthly':
        start_date = now().date().replace(day=1)
        end_date = now().date()
    elif report_type == 'custom':
        # Lire les dates depuis les paramètres GET
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if not start_date or not end_date:
                raise ValueError("Les dates de début et de fin doivent être fournies pour un rapport personnalisé.")
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError as e:
            return render(request, 'Manager/rapport_pointage.html', {'error': str(e)})
    else:
        return render(request, 'Manager/rapport_pointage.html', {'error': 'Type de rapport invalide.'})


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

    return render(request, 'Manager/rapport_pointage.html', {
        'report_type': report_type,
        'grouped_data': grouped_data,
        'start_date': start_date,
        'end_date': end_date,
    })
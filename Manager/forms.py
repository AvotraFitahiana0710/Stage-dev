from django import forms
from datetime import datetime, timedelta
from Administrateur.models import Departement, Person
from Manager.models import Shift, Pointage


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone_number', 'status', 'email', 'department', 'date_of_birth', 'cin', 'job_title', 'address']

        widgets = {
            'first_name' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer Prénom(s)',
                    'class':'form-control',
                }),
            'last_name' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer nom',
                    'class':'form-control'
                }),
            'phone_number' : forms.NumberInput(
                attrs = {
                    'placeholder' : 'Entrer numéro téléphone',
                    'class':'form-control'
                }),
            'status' : forms.Select(
                attrs = {
                    'class':'form-control'
                }),
            'email' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer email',
                    'class':'form-control',
                    'type' : 'email'
                }),
            'department' : forms.Select(
                attrs = {
                    'class':'form-control'
                }),
            'date_of_birth' : forms.DateInput(
                attrs = {
                    'class':'form-control',
                    'type' : 'date'
                }),
            'cin' : forms.NumberInput(
                attrs = {
                    'placeholder' : 'Entrer numéro CIN',
                    'class':'form-control'
                }),
            'job_title' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer titre de job',
                    'class':'form-control'
                }),
            'address' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer adresse',
                    'class':'form-control'
                }),
        }

        def __init__(self, *args, **kwargs):
            super(PersonForm, self).__init__(*args, **kwargs)
            self.fields['first_name'].error_messages = {
                'required' : 'Champ obligatoire',
                'invalid' : 'Champ invalide'
            }


#forms.NumberInput si de type number
#forms.Textarea si textarea, ave row : chiffre
#forms.DateInput si date et ajouter type : date
#forms.FileInput si image




class PointageForm(forms.ModelForm):
    class Meta:
        model = Pointage
        fields = ['check_in', 'check_out', 'shift', 'status']
        widgets = {
            'check_in' : forms.TimeInput(
                attrs = {
                    'type' : 'time',
                    'class':'form-control'
                }),
            'check_out' : forms.TimeInput(
                attrs = {
                    'type' : 'time',
                    'class':'form-control'
                }),
            'shift' : forms.Select(
                attrs = {
                    'class':'form-control'
                }),
            'status' : forms.Select(
                attrs = {
                    'class':'form-control'
                })
        }
        


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['name', 'manager']
        widgets = {
            'name' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer nom du département',
                    'class':'form-control'
                }),
            'manager' : forms.Select(
                attrs = {
                    'class':'form-control'
                })            
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['name', 'start_time', 'end_time', 'break_duration']
        widgets = {
            'name' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer nom du shift',
                    'class':'form-control'
                }),
            'start_time' : forms.TimeInput(
                attrs = {
                    'type' : 'time',
                    'class':'form-control'
                }),
            'end_time' : forms.TimeInput(
                attrs = {
                    'type' : 'time',
                    'class':'form-control'
                }),
            'break_duration' : forms.NumberInput(
                attrs = {
                    'class':'form-control'
                })
        }
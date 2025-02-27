from django import forms
from datetime import datetime, timedelta
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser
from django.contrib.auth.hashers import make_password

class AdminCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']


class UserAccountCreationForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['employee','email', 'username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(
                attrs = {
                    'placeholder' : 'Entrer mot de passe',
                    'class':'form-control'
                }),
            'username' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer nom d\'utilisateur',
                    'class':'form-control'
                }),
            'employee' : forms.Select(
                attrs = {
                    'class':'form-control'
                }),
            'email' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Entrer email',
                    'type' : 'emaill',
                    'class':'form-control'
                }),
            'role' : forms.Select(
                attrs = {
                    'class':'form-control'
                })
        }
            

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hachage du mot de passe
        if commit:
            user.save()
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserAccount.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet e-mail existe déjà.")
        return email

class UserAccountLoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin, Group, Permission
from datetime import datetime, timedelta



# Create your models here.
# class CustomUser(AbstractUser):
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name="customuser_groups",  # Ajoutez un related_name unique
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="customuser_user_permissions",  # Ajoutez un related_name unique
    #     blank=True
    # )
    # is_admin = models.BooleanField(default=False)  # Indique si l'utilisateur est un administrateur
    # username = models.CharField(max_length=100, unique=True, verbose_name="Nom d'utilisateur")
    # email = models.EmailField(max_length=255, unique=True, verbose_name="Adresse email")



class Departement(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du département")
    manager = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departements')

    def __str__(self):
        return self.name

class UserAccountManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, employee=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire")

        # Vérifier si l'utilisateur n'est pas un superutilisateur
        if not extra_fields.get('is_superuser', False) and not employee:
            raise ValueError("Le champ 'employee' est obligatoire pour les utilisateurs normaux")

        # Si l'email est fourni, normalisez-le
        email = self.normalize_email(email) if email else None

        user = self.model(
            username=username,
            email=email,
            employee=employee,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")

        # Appeler create_user sans fournir le champ employee
        return self.create_user(username=username, email=email, password=password, employee=None, **extra_fields)
         
class UserAccount(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Admin', 'Administrateur'),
        ('Manager', 'Manager'),
        ('Employee', 'Employé'),
    ]
    # employee = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='user_account')
    employee = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='user_account', null=True, blank=True)
    #employee = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='user_account')

    username = models.CharField(max_length=100, unique=True, verbose_name="Nom d'utilisateur")
    password = models.CharField(max_length=255, verbose_name="Mot de passe")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Manager', verbose_name="Rôle utilisateur")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Adresse email", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)  # Indique si l'utilisateur est un administrateur


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    objects = UserAccountManager()

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        """
        Vérifie si l'utilisateur a une permission spécifique.
        Par défaut, tous les utilisateurs actifs ont toutes les permissions.
        """
        if self.role == "Admin" or self.role == "Manager":
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        """
        Vérifie si l'utilisateur a des permissions pour une application spécifique.
        Par défaut, tous les utilisateurs actifs ont accès à toutes les applications.
        """
        if self.role == "Admin" or self.role == "Manager":
            return True
        else:
            return False

class Person(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Actif'),
        ('Inactive', 'Inactif'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True, verbose_name="Adresse email")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active', verbose_name="Statut")
    department = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    cin = models.CharField(max_length=20, unique=True, verbose_name="Numéro CIN")
    job_title = models.CharField(max_length=100, verbose_name="Titre de job")
    address = models.TextField(verbose_name="Adresse")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 
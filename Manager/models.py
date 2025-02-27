from django.db import models
from Administrateur.models import Person, Departement
from datetime import datetime, timedelta
from django.utils.timezone import now

# Create your models here.
class Shift(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nom du Shift")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    break_duration = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name="Durée de pause (en heures)")
    
    def __str__(self):
        return self.name


class Pointage(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Présent'),
        ('Absent', 'Absent'),
        ('Late', 'En retard'),
        ('Excused', 'Excusé'),
        ('Cong', 'Congé'),
    ]
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Pointage')
    date_pointage = models.DateField(verbose_name="Date du pointage", auto_now_add=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)#comparaison avec Shift pour heure sup ou sanction
    check_in = models.TimeField(null=True, blank=True, verbose_name="Heure d'entrée")
    check_out = models.TimeField(null=True, blank=True, verbose_name="Heure de sortie")
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Heures travaillées")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present', verbose_name="Statut")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['person', 'date_pointage'], name='unique_pointage_per_employee')
        ]

        
    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            check_in_datetime = datetime.combine(self.date_pointage, self.check_in)
            check_out_datetime = datetime.combine(self.date_pointage, self.check_out)
            total_hours = (check_out_datetime - check_in_datetime).total_seconds() / 3600  # Convertir en heures
            total_hours -= float(self.person.department.break_duration if self.person.department else 0)  # Retirer la pause si applicable
            self.hours_worked = max(total_hours, 0)  # Éviter les valeurs négatives
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pointage de {self.person} le {self.date_pointage}"


    def __str__(self):
        return self.username

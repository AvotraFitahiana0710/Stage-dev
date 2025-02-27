from django.contrib import admin
from .models import UserAccount, Person, Departement
# Register your models here.

# admin.site.register(CustomUser)
admin.site.register(UserAccount)
admin.site.register(Person)
admin.site.register(Departement)
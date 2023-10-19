from django.contrib import admin
from application.models import ColSante, ColStress


class ColonnesStress(admin.ModelAdmin):
    #list_display = ("id", "username", "role", "email","is_superuser",)  #[field.name for field in Utilisateur._meta.get_fields()]
    list_display = [field.name for field in ColStress._meta.get_fields()]

class ColonnesSante(admin.ModelAdmin):
    #list_display = ("id", "username", "role", "email","is_superuser",)  #[field.name for field in Utilisateur._meta.get_fields()]
    list_display = [field.name for field in ColSante._meta.get_fields()]

admin.site.register(ColStress, ColonnesStress)
admin.site.register(ColSante, ColonnesSante)
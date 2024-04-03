"""
URL configuration for djangolib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application.views import *
from authentification.views import *
from api.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accueil", accueil, name="accueil"),
    path("", connexion, name="connexion"),
    path("deco", deco, name="deco"),
    path("inscription", inscription, name="inscription"),
    path('data_stress/', data_stress, name='data_stress'),
    path("association", association, name="association"),
    path('comptes/', comptes, name='comptes'),
    path('data_sante', data_sante, name="data_sante"),
    path('sante_datatable', sante_datatable, name="sante_datatable"),
    path('stress_datatable', stress_datatable, name="stress_datatable"),
    path('histo_patient', histo_patient, name="histo_patient"),
    path('edaia', edaia, name="edaia"),
    path('get_last_username/<str:role>/', get_last_username, name='get_last_username'),
    path('nouveau_compte', nouveau_compte, name="nouveau_compte"),
    path("qanda/", qanda, name="qanda"),
]


#
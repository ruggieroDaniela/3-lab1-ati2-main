from django.urls import path
from . import views

urlpatterns = [
    path('cambiar-nombre/', views.cambiarNombre,name="cambiar-nombre")
]

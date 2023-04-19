import os
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from lab_ati.cliente.forms import ClienteForm
from lab_ati.cliente.models import Cliente
from lab_ati.empresa.forms import SocialMediaFormset
from lab_ati.empresa.models import SocialMedia
from lab_ati.utils.social_media import add_social_media
from django.urls import reverse
import requests


def cambiarNombre(request):
    if request.method == 'POST':
        # Obtener el nuevo nombre del POST
        new_value = request.POST["new-value"]

        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = os.path.join(BASE_DIR, 'nombre.txt')
        with open(file_path, 'w') as f:
            f.write(new_value)
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="nombre.txt"'
    
    return redirect('/')


def getCountries():
    countries = requests.get("https://restcountries.com/v3.1/all?fields=name").json()      # Get information about countries via a RESTful API
    names = []
    for i in countries:
        names.append(i["name"]["common"])

    names = sorted(names)
    return names


def clientes(request, business_id):
    context = {}
    context['business_id'] = business_id
    clientes = Cliente.objects.filter(empresa__id__contains = business_id)
    context['clientes'] = clientes
    return render(request, 'pages/clientes/index.html', context)

def ver_cliente(request, id, business_id):
    context = {}
    context['business_id'] = business_id
    cliente = Cliente.objects.get(id = id)
    context['form'] = ClienteForm(request.POST or None, instance=cliente)
    context['social_medias'] = cliente.redes_sociales.all()
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    return render(request, 'pages/clientes/verCliente.html', context)

def crear_cliente(request, business_id):
    context = {}
    context['business_id'] = business_id
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        savedForm = form.save()
        social_media_formset = SocialMediaFormset(data=request.POST)
        if social_media_formset.is_valid():
            add_social_media(savedForm, social_media_formset)
        return redirect('clients', business_id = business_id)
    context['form'] = form
    context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context['business_id'] = business_id
    context['paises'] = getCountries()
    return render(request, 'pages/clientes/crear.html', context)


def eliminar_cliente(request, id, business_id):
    cliente = Cliente.objects.get(id = id)
    cliente.delete()
    context = {}
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context['business_id'] = business_id
    return redirect('clients', business_id = business_id)

def editar_cliente(request, id, business_id):
    context = {}
    context['business_id'] = business_id
    cliente = Cliente.objects.get(id = id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid() and request.POST:
        savedForm = form.save()
        social_media_formset = SocialMediaFormset(data=request.POST, queryset=savedForm.redes_sociales.all())
        if social_media_formset.is_valid():
            add_social_media(savedForm, social_media_formset)

        return redirect('clients', business_id = business_id)
    context['form'] = form
    context["socialm_formset"] = SocialMediaFormset(queryset=cliente.redes_sociales.all())
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context["editing_social"] = True
    context['paises'] = getCountries()
    
    return render(request, 'pages/clientes/editar.html', context)

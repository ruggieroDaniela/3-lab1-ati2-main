from django.http.response import Http404
from django.urls.base import reverse_lazy

from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView
from .forms import CreateBusinessForm, CreateEmployeeForm, SocialMediaFormset
from lab_ati.empresa.models import Empleado, Empresa, SocialMedia
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core import exceptions
from django.shortcuts import render
from lab_ati.utils.social_media import add_social_media
from django.urls import reverse
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import requests

def cambiarNombre(request):
    if request.method == 'POST':
        # Obtener el nuevo nombre del POST
        nuevo_nombre = request.POST.get('nuevo_nombre')
        
        # Realizar la lógica para cambiar el nombre
        # ...
        
        # Enviar una respuesta exitosa
        return HttpResponse('El nombre ha sido cambiado exitosamente')


def getCountries():
    countries = requests.get("https://restcountries.com/v3.1/all?fields=name").json()      # Get information about countries via a RESTful API
    names = []
    for i in countries:
        names.append(i["name"]["common"])

    names = sorted(names)
    return names

# Businesses Views
class BusinessListView(ListView):
    template_name = "pages/business/list.html"
    model = Empresa
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open('lab_ati/nombre.txt', 'r') as archivo:
            contenido = archivo.read()

        
        context['mi_variable'] = contenido
        return context


class BusinessDetailsView(DetailView):
    template_name = "pages/business/detail.html"
    model = Empresa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["business_id"] = self.object.id
        context["list_link"] = "/business"
        return context
    
class CreateBusinessView(CreateView):
    template_name = "pages/business/create.html"
    model = Empresa
    form_class = CreateBusinessForm

    def get_success_url(self):
        return reverse("empresa:business-list")

    def post(self, request, *args, **kwargs):
        self.object = None

        self.social_media_formset = SocialMediaFormset(data = self.request.POST)
        
        #Call parent class post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.social_media_formset.is_valid():
            return self.form_invalid(form)
        res = super().form_valid(form)
        # Add social media to Empresa
        add_social_media(self.object, self.social_media_formset)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Header
        context["list_link"] = "/business"

        # Queryset vacio porque vamos a crear una empresa nuevo
        context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
        return context

class EditBusinessView(UpdateView):
    template_name = "pages/business/create.html"
    model = Empresa
    form_class = CreateBusinessForm
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse("empresa:business-list")
    
    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.social_media_formset = SocialMediaFormset(
            data=self.request.POST,
            queryset=self.object.redes_sociales.all()
        )
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        if not self.social_media_formset.is_valid():
            return self.media_form_invalid(form)

        # Update and add social media
        add_social_media(self.object, self.social_media_formset)

        res = super().form_valid(form)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def media_form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["socialm_formset"] = SocialMediaFormset(
            queryset=self.object.redes_sociales.all()
        )
        context["editing_social"] = True
        context["business_id"] = self.object.id

        #Header
        context["list_link"] = "/business"
        return context

class DeleteBusinessView(DeleteView):
    template_name = "pages/business/delete.html"
    model = Empresa

    def get_success_url(self):
        return reverse('empresa:business-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_link"] = "/business"
        return context

    

#Employees Views
class ListEmployeeView(ListView):
    template_name = "pages/employees/list.html"
    model = Empleado
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        return context

    def get_queryset(self):
        queryset = Empleado.objects.filter(empresa = self.kwargs['business_id'])
        return queryset

class DetailEmployeeView(DetailView):
    template_name = "pages/employees/detail.html"
    model = Empleado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']

        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["business_id"]} )
        return context
    
class CreateEmployeeView(CreateView):
    template_name = "pages/employees/create.html"
    model = Empleado
    form_class = CreateEmployeeForm

    def get_success_url(self):
        return reverse(
            "empresa:edit-employee",
            kwargs={
                "business_id": self.empresa.id,
                "pk": self.object.pk,
            },
        )
    
    def get_empresa(self):
        # Validate that Empresa exists
        try:
            empresa = Empresa.objects.get(id=self.kwargs.get("business_id"))
        except (Empresa.DoesNotExist, exceptions.ValidationError):
            raise Http404(_("La empresa no existe"))
        return empresa

    def post(self, request, *args, **kwargs):
        self.object = None

        # Validate that Empresa exists
        self.empresa = self.get_context_data()["empresa"]

        self.social_media_formset = SocialMediaFormset(data=self.request.POST)

        # Call parent class post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Override form valid method to add socialmedia
        # functionality

        if not self.social_media_formset.is_valid():
            return self.form_invalid(form)

        res = super().form_valid(form)
        # Add social media to Empleado
        add_social_media(self.object, self.social_media_formset)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        context["empresa"] = self.get_empresa()
        context["business_id"] = context["empresa"].id

        # Get countries        
        context["paises"] = getCountries()

        # Header
        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["empresa"].id} )

        # Queryset vacio porque vamos a crear un empleado nuevo
        context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
        return context

class EditEmployeeView(UpdateView):
    template_name = "pages/employees/create.html"
    model = Empleado
    form_class = CreateEmployeeForm
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse(
            "empresa:edit-employee",
            kwargs={
                "business_id": self.empresa.id,
                "pk": self.object.pk,
            },
        )

    def get_empresa(self):
        # Validate that Empresa exists
        try:
            empresa = Empresa.objects.get(id=self.kwargs.get("business_id"))
        except (Empresa.DoesNotExist, exceptions.ValidationError):
            raise Http404(_("La empresa no existe"))
        return empresa

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.empresa = self.get_empresa()
        self.social_media_formset = SocialMediaFormset(
            data=self.request.POST,
            queryset=self.object.redes_sociales.all()
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        if not self.social_media_formset.is_valid():
            return self.media_form_invalid(form)

        # Update and add social media
        add_social_media(self.object, self.social_media_formset)

        res = super().form_valid(form)
        return res

    def media_form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        context["empresa"] = self.get_empresa()
        context["socialm_formset"] = SocialMediaFormset(
            queryset=self.object.redes_sociales.all()
        )
        context["editing_social"] = True

        # Get countries         
        context["paises"] = getCountries()
        
        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["empresa"].id} )
        return context

class DeleteEmployeeView(DeleteView):
    template_name = "pages/employees/delete.html"
    model = Empleado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']

        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["business_id"]} )
        return context

    def get_success_url(self):
        return reverse('empresa:list-employee', kwargs={ 'business_id': self.kwargs['business_id']})

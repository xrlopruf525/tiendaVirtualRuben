from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse_lazy
from .forms import *
# Create your views here.

class Inicio(TemplateView):
    template_name = "tienda/inicio.html"
    
class ListadoProductos(ListView):
    model = Producto
    template_name = 'tienda/listadoProductos.html'
    context_object_name = 'productos'
class EditarProducto(UpdateView):
    model = Producto
    form_class= ProductoEditarForm
    template_name = 'tienda/productoeditar.html'
    success_url = reverse_lazy('listadoProductos')
    
class EliminarProducto(DeleteView):
    model = Producto
    template_name = 'tienda/eliminarProducto.html'
    success_url = reverse_lazy('listadoProductos')
class CrearProducto(CreateView):
    model = Producto
    template_name = 'tienda/crearProducto.html'
    fields = ['nombre','modelo','unidades','precio','vip','marca' ]
    success_url = reverse_lazy('listadoProductos')


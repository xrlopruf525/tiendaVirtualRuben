from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class Inicio(TemplateView):
    template_name = "tienda/inicio.html"
    
class ListadoProductos(ListView):
    model = Producto
    template_name = 'tienda/listadoProductos.html'
    context_object_name = 'productos'
class EditarProducto(LoginRequiredMixin,UpdateView):
    model = Producto
    form_class= ProductoEditarForm
    template_name = 'tienda/productoeditar.html'
    success_url = reverse_lazy('listadoProductos')
    
class EliminarProducto(LoginRequiredMixin,DeleteView):
    model = Producto
    template_name = 'tienda/eliminarProducto.html'
    success_url = reverse_lazy('listadoProductos')
    
class CrearProducto(LoginRequiredMixin,CreateView):
    model = Producto
    template_name = 'tienda/crearProducto.html'
    fields = ['nombre','modelo','unidades','precio','vip','marca' ]
    success_url = reverse_lazy('listadoProductos')

class ComprarProducto(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'tienda/compra_listado.html'
    context_object_name = 'productos'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['marcas'] = Marca.objects.all()  
        return contexto

    def get_queryset(self):
        query = super().get_queryset()
        nombre = self.request.GET.get("filtro_nombre")
        marca = self.request.GET.get("filtro_marca")
        precio = self.request.GET.get("filtro_precio")

        if nombre:
            query = query.filter(nombre__icontains=nombre)
        if marca:
            query = query.filter(marca__nombre=marca)
        if precio:
            query = query.filter(precio__lte=precio)

        return query
    
class Checkout(LoginRequiredMixin, View):
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        unidades = int(request.GET.get('unidades', 1))
        total = unidades * producto.precio
        return render(request, 'tienda/checkout.html', {'producto': producto, 'unidades': unidades, 'total': total})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        unidades = int(request.POST.get('unidades'))
        usuario = request.user
        total = unidades * producto.precio

        if usuario.saldo >= total and unidades <= producto.unidades:
            Compra.objects.create(usuario=usuario, producto=producto, unidades=unidades, importe=total)
            usuario.saldo -= total
            usuario.save()
            producto.unidades -= unidades
            producto.save()
            messages.success(request, "Compra realizada correctamente")
        else:
            messages.error(request, "No hay suficiente saldo o unidades")

        return redirect('compra_listado')
    
def checkout(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']
            if unidades > producto.unidades:
                 form.add_error('unidades', 'No hay suficientes unidades disponibles.')
            else:
                 importe = unidades * producto.precio
                 Compra.objects.create(
                     usuario=request.user,
                     producto=producto,
                     unidades=unidades,
                     importe=importe, 
                 )
                 producto.unidades -= unidades
                 producto.save()
                 return redirect('compra_listado') 
    else:
         form = CompraForm()
    return render(request, 'tienda/checkout.html', {'producto': producto, 'form': form})

class CheckoutProducto(CreateView):
     model=Compra
     form_class=CompraForm
     template_name='tienda/checkout.html'
     success_url=reverse_lazy('compra_listado')

     def get_context_data(self, **kwargs):
         context=super().get_context_data(**kwargs)
         context['producto']=get_object_or_404(Producto,pk=self.kwargs['pk'])
         return context
    
    
     def form_valid(self, form):
         producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
         unidades = form.cleaned_data['unidades']
        
         if producto.unidades < unidades:
             form.add_error('unidades', 'No hay suficientes unidades disponibles.')
             return self.form_invalid(form)
            
         compra = form.save(commit=False)
         compra.producto = producto
         compra.usuario = self.request.user
         compra.importe = producto.precio * unidades
        
         producto.unidades -= unidades
         producto.save()
        
         compra.save()
        
         # Actualizar saldo del usuario
         usuario = self.request.user
         usuario.saldo -= compra.importe 
         usuario.save()
         print("FORM VALID EJECUTADO")

        
         return super().form_valid(form)
    
@staff_member_required
def informes(request):
    topclientes = Usuario.objects.annotate(total_gastado=Sum('compra__importe')).order_by('-total_gastado')[:10]
    topproductos = Producto.objects.annotate(total_vendidos=Sum('compra__unidades')).order_by('-total_vendidos')[:10]
    return render(request, 'tienda/informes.html', {'topclientes': topclientes, 'topproductos': topproductos})

class PerfilView(LoginRequiredMixin, ListView):
    model = Compra
    paginate_by = 4
    template_name = 'tienda/perfil.html'

    def get_queryset(self):
        return Compra.objects.filter(usuario=self.request.user)
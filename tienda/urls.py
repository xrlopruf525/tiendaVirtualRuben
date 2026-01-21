from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", views.Inicio.as_view(), name = "inicio"),
    path("listadoProductos/",views.ListadoProductos.as_view(), name = 'listadoProductos'),
    path("producto/<int:pk>/editar/", views.EditarProducto.as_view(), name='producto_editar'),
    path("producto/<int:pk>/eliminar/", views.EliminarProducto.as_view(), name='producto_eliminar'),
    path("producto/nuevo",views.CrearProducto.as_view(), name='producto_crear'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tienda/', ComprarProducto.as_view(), name='compra_listado'),
    path('checkout/<int:pk>/', Checkout.as_view(), name='checkout'),
    path('S/', informes, name='informes'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    
]

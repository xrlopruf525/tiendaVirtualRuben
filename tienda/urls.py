from django.urls import path
from . import views

urlpatterns = [
    path("", views.Inicio.as_view(), name = "inicio"),
    path("listadoProductos/",views.ListadoProductos.as_view(), name = 'listadoProductos'),
    path("producto/<int:pk>/editar/", views.EditarProducto.as_view(), name='producto_editar'),
    path("producto/<int:pk>/eliminar/", views.EliminarProducto.as_view(), name='producto_eliminar'),
    path("producto/nuevo",views.CrearProducto.as_view(), name='producto_crear')
    
]

from django import forms
from .models import *

class ProductoEditarForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','modelo','unidades','precio','vip','marca' ]


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = "__all__"
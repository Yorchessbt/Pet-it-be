from django import forms
from .models import Pet, Comentario, Solicitud

class AddPets(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('especie', 'name', 'descripcion', 'image', 'edad', 'status')

        widgets ={
            'especie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre de la mascota',
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Agrega informacion de tu mascota',
                'class': 'form-control',
                'style': 'height: 116px'
            }),
           'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),    
        }

class RequestForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['direccion', 'edad', 'telefono', 'ocupacion', 'estado', 'salario']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 18,
                'placeholder': 'Tu edad'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 55 1234 5678'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Cantidad en pesos'
            }),
        }         


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['text']
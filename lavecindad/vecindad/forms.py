from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django.contrib.auth import get_user_model  # Importa get_user_model
from django.db import models

from vecindad.validators import validate_rut
from .models import JuntaDeVecinos, Mensaje, NoticiaJuntaVecinos, UsuarioPersonalizado


class AlgunaClase(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    

class RegistroForm(UserCreationForm):
    rut = forms.CharField(
        label="RUT",
        max_length=20,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        },
        validators=[validate_rut],  # Aplicar la misma validación personalizada
    ) 
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=True,
         error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )
    
    direccion = forms.CharField(max_length=255, required=True, error_messages={
            'required': 'Este campo es obligatorio.',
        })
    sexo = forms.ChoiceField(
        choices=[('', 'Sexo'), ('M', 'Masculino'), ('F', 'Femenino')],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control custom-select'}),
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    first_name = forms.CharField(
        label="Nombre",  # Cambia la etiqueta aquí
        max_length=30,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    last_name2 = forms.CharField(
        max_length=30,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )
    username = forms.CharField(
        label="Nombre de usuario",  # Cambia la etiqueta aquí
        max_length=30,
        required=True,
        
    )
    telefono = forms.CharField(max_length=15, required=False, error_messages={
            'required': 'Este campo es obligatorio.',
        })  # Agregar el campo de número de teléfono


    junta_de_vecinos = forms.ModelChoiceField(
        queryset=JuntaDeVecinos.objects.all(),
        widget=forms.Select(attrs={'class': 'select-field', 'style': 'border: none;'}),
        required=False,
       
    )

    id_sede = forms.CharField(
        label="ID de Sede",  # Cambia la etiqueta aquí
        max_length=20,
        required=False,
        
    )

    
    class Meta:
        model = get_user_model()  # Utiliza get_user_model()
        fields = ('rut','username' , 'first_name','last_name','last_name2','email','fecha_nacimiento', 'direccion', 'sexo','telefono','id_sede','junta_de_vecinos','password1', 'password2',)
        help_text = {k:"" for k in fields }

    
    def __init__(self, *args, **kwargs):
        
        super(RegistroForm, self).__init__(*args, **kwargs)
 
        
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        
class InicioSesionForm(AuthenticationForm):
    class Meta:
        model = get_user_model()  # Utiliza get_user_model()
        fields = ['username', 'password']

class EditProfileForm(UserChangeForm):

    password = None  # Excluye el campo de contraseña

    class Meta:
        model = UsuarioPersonalizado  # Utiliza tu modelo de usuario personalizado
        fields = ['email', 'direccion', 'telefono']  # Lista los campos que deseas editar
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza la etiqueta del campo de correo electrónico
        self.fields['email'].label = 'Email'



class NoticiaForm(forms.ModelForm):
    class Meta:
        model = NoticiaJuntaVecinos
        fields = ['imagen', 'titulo', 'contenido']



class MensajeForm(forms.ModelForm):
    
    class Meta:
        model = Mensaje
        fields = ['contenido', 'solicitud_espacios','solicitud_fecha_hora']

    solicitud_fecha_hora = forms.DateTimeField(
        label='Solicitar Fecha y Hora',  # Etiqueta personalizada para el campo
        required=False,  # Puedes ajustar esto según tus necesidades
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

class MensajeModalForm(forms.ModelForm):

    class Meta:
        model = Mensaje
        fields = ['asunto','contenido_presidente']  # Agrega los campos de asunto y contenido_presidente

    def __init__(self, *args, **kwargs):
        super(MensajeModalForm, self).__init__(*args, **kwargs)

        # Puedes personalizar los widgets o agregar clases CSS a los campos si es necesario
        self.fields['asunto'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['contenido_presidente'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})


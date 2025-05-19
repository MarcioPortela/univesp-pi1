from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Digite seu nome de usuário'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu e-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'

        # Traduzindo as mensagens de erro
        self.fields['username'].error_messages = {
            'unique': 'Este nome de usuário já está em uso.',
            'invalid': 'Digite um nome de usuário válido.',
            'required': 'O nome de usuário é obrigatório.',
        }
        self.fields['email'].error_messages = {
            'invalid': 'Digite um endereço de e-mail válido.',
            'required': 'O e-mail é obrigatório.',
        }
        self.fields['password1'].error_messages = {
            'required': 'A senha é obrigatória.',
        }
        self.fields['password2'].error_messages = {
            'required': 'A confirmação de senha é obrigatória.',
            'password_mismatch': 'As senhas não conferem.',
        }

class ProfileForm(forms.ModelForm):
    STATE_CHOICES = [
        ('', 'Selecione um estado'),
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'city', 'state', 'zip_code']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX-XXX'}),
        }
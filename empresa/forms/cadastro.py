from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CadastroForm(forms.ModelForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = [
            'nome',
            'email',
            'senha',
            'confirmar_senha',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email já existe')
        return email

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha != confirmar_senha:
            raise ValidationError({
                'confirmar_senha': 'senha e confirmar senha não são iguais'
            })

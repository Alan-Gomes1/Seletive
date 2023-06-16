from django import forms


class LoginForm(forms.Form):
    nome = forms.CharField(max_length=100)
    senha = forms.CharField(
        widget=forms.PasswordInput(),
    )

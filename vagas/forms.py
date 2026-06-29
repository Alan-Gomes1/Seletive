from django import forms
from django.core.exceptions import ValidationError
from empresa.models import Vagas


class VagaForm(forms.ModelForm):
    tecnologias_estudar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Tecnologias a estudar"}),
    )

    class Meta:
        model = Vagas
        fields = [
            "titulo",
            "email",
            "nivel_experiencia",
            "data_final",
            "empresa",
            "status",
            "tecnologias_dominadas",
            "tecnologias_estudar",
        ]

    def clean_titulo(self) -> str:
        """
        Valida o título da vaga para garantir que tenha pelo menos
        5 caracteres.

        Raises:
            ValidationError: Título must be at least 5 characters.

        Returns:
            str: O título da vaga validado.
        """
        titulo = self.cleaned_data["titulo"]
        if len(titulo.strip()) < 5:
            raise ValidationError("Título must be at least 5 characters.")
        return titulo

    def clean_email(self) -> str:
        """
        Valida o e-mail da vaga para garantir que tenha pelo menos
        5 caracteres.

        Raises:
            ValidationError: Email must be at least 5 characters.

        Returns:
            str: O e-mail da vaga validado.
        """
        email = self.cleaned_data["email"]
        if len(email.strip()) < 5:
            raise ValidationError("Email must be at least 5 characters.")
        return email

    def clean_nivel_experiencia(self) -> str:
        """
        Valida o nível de experiência para garantir que tenha pelo menos
        1 caractere.

        Raises:
            ValidationError: Experience level is required.

        Returns:
            str: O nível de experiência validado.
        """
        experience = self.cleaned_data["nivel_experiencia"]
        if len(experience.strip()) < 1:
            raise ValidationError("Experience level is required.")
        return experience

    def clean_empresa(self):
        """
        Valida que a empresa foi selecionada.

        Raises:
            ValidationError: Empresa is required.

        Returns:
            Empresa: A empresa validada.
        """
        empresa = self.cleaned_data["empresa"]
        if not empresa:
            raise ValidationError("Empresa is required.")
        return empresa

    def clean_status(self) -> str:
        """
        Valida o status para garantir que tenha pelo menos
        1 caractere.

        Raises:
            ValidationError: Status is required.

        Returns:
            str: O status validado.
        """
        status = self.cleaned_data["status"]
        if len(status.strip()) < 1:
            raise ValidationError("Status is required.")
        return status

    def clean_data_final(self):
        """
        Valida que a data final foi preenchida.

        Raises:
            ValidationError: Data final is required.

        Returns:
            date: A data final validada.
        """
        data_final = self.cleaned_data["data_final"]
        if not data_final:
            raise ValidationError("Data final is required.")
        return data_final

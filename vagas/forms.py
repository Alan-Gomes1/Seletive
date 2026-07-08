from django import forms
from django.core.exceptions import ValidationError
from empresa.models import Vagas, Tecnologias
from vagas.models import Tarefas


class VagaForm(forms.ModelForm):
    tecnologias_estudar = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tecnologias.objects.all(),
        widget=forms.CheckboxInput,
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

    def clean_empresa(self) -> str:
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


class TarefasForm(forms.ModelForm):
    class Meta:
        model = Tarefas
        fields = ["titulo", "prioridade", "data"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Task title"}),
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_titulo(self) -> str:
        """
        Validate the task title to ensure it has at least 5 characters.

        Raises:
            ValidationError: Title must be at least 5 characters.

        Returns:
            str: The validated task title.
        """
        title = self.cleaned_data["titulo"]
        if len(title.strip()) < 5:
            raise ValidationError("Title must be at least 5 characters.")
        return title

    def clean_prioridade(self) -> str:
        """
        Validate the priority level to ensure it has exactly 1 character.

        Raises:
            ValidationError: Priority is required and must be A, B, or U.

        Returns:
            str: The validated priority (A, B, or U).
        """
        prioridade = self.cleaned_data["prioridade"]
        if len(prioridade.strip()) != 1:
            raise ValidationError(
                "Priority is required and must be A, B, or U."
            )
        return prioridade

    def clean_data(self):
        """
        Validate that a date was filled.

        Raises:
            ValidationError: Date is required.

        Returns:
            date: A validated date.
        """
        data = self.cleaned_data["data"]
        if not data:
            raise ValidationError("Date is required.")
        return data

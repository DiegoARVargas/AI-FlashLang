from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """
    Formulario para crear nuevos usuarios en el admin.
    Incluye dos campos de contraseña con validación.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    class Meta:
        model = CustomUser
        fields = ("email", "username", "preferred_language", "is_premium")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegura que los campos no se autocompleten entre sí
        self.fields["username"].widget.attrs.update({"autocomplete": "off"})
        self.fields["email"].widget.attrs.update({"autocomplete": "off"})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para actualizar usuarios desde el admin.
    Muestra la contraseña como un hash solo lectura.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "preferred_language", "is_premium", "is_active", "is_staff", "is_superuser")

    def clean_password(self):
        return self.initial["password"]
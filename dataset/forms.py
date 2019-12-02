from django import forms


class UsuarioBusquedaForm(forms.Form):
    id_usuario = forms.CharField(
        label="Id de Usuario",
        widget=forms.TextInput,
        required=True
    )


class PeliculaBusquedaYearForm(forms.Form):
    year = forms.IntegerField(
        label="Año de publicación",
        widget=forms.TextInput,
        required=True
    )

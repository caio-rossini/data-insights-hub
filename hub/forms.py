from django import forms
from django.contrib.auth import get_user_model


class AnalysisProjectSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search projects by title..."
        })
    )


class DataAnalystSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search analysts by username..."
        })
    )


class DatasetSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search datasets by name..."
        })
    )


class AnalysisDomainSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search domains by name..."
        })
    )


class DataAnalystCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter a secure password"
        }),
        label="Password"
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username", "email", "password", "first_name", "last_name", "position"
        ]

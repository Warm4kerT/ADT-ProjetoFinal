from django import forms
from .models import Router, Script
from .functions import unique, prepare_choices

class RawRouterForm(forms.Form):
    name = forms.CharField(max_length=25)
    localization = forms.CharField(max_length=25)
    model = forms.CharField(max_length=25)
    ip = forms.GenericIPAddressField()
    porta = forms.IntegerField()
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=30,
        widget=forms.PasswordInput())

class RawScriptForm(forms.Form):
    model_choices = prepare_choices(Router.objects.values_list('model'))
    name = forms.CharField(max_length=25)
    version = forms.DecimalField(max_digits=10, decimal_places=2)
    compatible_model = forms.CharField(
        widget=forms.Select(choices=model_choices))
    file = forms.FileField()

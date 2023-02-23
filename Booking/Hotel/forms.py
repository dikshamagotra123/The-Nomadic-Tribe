from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label=_("First name"))
    last_name = forms.CharField(max_length=30, label=_("Last name"))
    display_name = forms.CharField(max_length=30, label=_("Display name"), help_text=_("Will be shown e.g. when commenting."))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.display_name = self.cleaned_data['display_name']
        user.save()
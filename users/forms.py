from django import forms
from .models import Role
from health.models import Team

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=15)
    name = forms.CharField(label="Full Name", max_length=50)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Select Role")
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Select Team", required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class LoginForm(forms.Form):
    identifier = forms.CharField(label="Username or Email", max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
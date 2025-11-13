from django import forms
from .models import (
    CustomUser,
    Events,
    Document,
    Organization
)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    
    def clean(self):
        clean_data = super().clean()
        print(clean_data)
        return clean_data


class RegisterForm(forms.ModelForm):
    
    retype_password = forms.CharField(
        label="Re-type your password.",
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'email',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def clean(self):
        clean_data = super().clean()
        
        password = clean_data.get('password')
        retype_password = clean_data.get('retype_password')
        
        if len(password) <= 8:
            raise forms.ValidationError("The password cannot be shorter..")
        
        if password != retype_password:
            raise forms.ValidationError("The password is not the same.")
        
        
        return clean_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
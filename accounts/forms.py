from django.forms import ModelForm, EmailInput, PasswordInput

from .models import MyUser

class MyUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ["email", "password"]
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'})
        }

from django.forms import ModelForm, TextInput, ImageField, EmailInput, \
                                                           PasswordInput

from .models import MyUser


class SignUpForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'avatar', 'email', 'password']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'})
        }

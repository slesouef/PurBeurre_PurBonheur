from django.forms import ModelForm, TextInput, EmailInput, PasswordInput

from .models import MyUser


class SignUpForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'avatar', 'email',
                  'password']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'})
        }

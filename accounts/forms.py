"""
Form used to allow the user to create an account
"""
from django.forms import ModelForm, TextInput, ClearableFileInput, \
                         EmailInput, PasswordInput

from .models import MyUser


class SignUpForm(ModelForm):
    """
    The form contains all the fields necessary to create an account
    Mandatory fields are:
        username, first_name, email, and password
    Optional fields are:
        last_name and avatar
    """

    class Meta:
        model = MyUser
        fields = ["username", "first_name", "last_name", "avatar", "email",
                  "password"]
        widgets = {
            "username": TextInput(attrs={"class": "form-control"}),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "avatar": ClearableFileInput(attrs={"class": "form-control-file"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "password": PasswordInput(attrs={"class": "form-control"}),
        }

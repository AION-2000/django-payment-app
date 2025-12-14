from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div
from django_recaptcha.fields import ReCaptchaField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    captcha = ReCaptchaField()
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'captcha')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('first_name', placeholder='First Name'),
            Field('last_name', placeholder='Last Name'),
            Field('password1', placeholder='Password'),
            Field('password2', placeholder='Confirm Password'),
            Field('captcha'),
            Div(
                Submit('submit', 'Sign Up', css_class='btn btn-primary w-100'),
                css_class='text-center'
            )
        )
        self.fields['email'].widget.attrs.update({'autofocus': True})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('password', placeholder='Password'),
            Field('captcha'),
            Div(
                Submit('submit', 'Log In', css_class='btn btn-primary w-100'),
                css_class='text-center'
            )
        )
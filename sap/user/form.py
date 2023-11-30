from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='Ingrese un correo válido', required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm,self).__init__(*args, **kwargs)
    
    username = forms.CharField(
        label='Nombre de usuario o correo electrónico',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de usuario o correo electrónico',})
    )
    password = forms.CharField(required=True,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Contraseña'}
    ))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Correo electrónico',})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email','image', 'description']



class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
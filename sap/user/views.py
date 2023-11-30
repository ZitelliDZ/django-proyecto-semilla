from django.shortcuts import render, redirect


from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from .decorators import user_not_authenticated
from .form import UserLoginForm, UserRegisterForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from .tokens import account_activation_token


def signup_redirect(request):
    messages.error(request, "Algo está mal aquí, puede ser que ya tengas una cuenta.")
    return redirect("homepage")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Ha confirmado su correo electrónico. Ahora puedes iniciar sesión en su cuenta.")
        return redirect('login')
    else:
        messages.error(request, "El enlace de activación no es válido.")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = 'Active su cuenta.'
    message = render_to_string(
        'user/mail/template_activate_account.html',
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject,message, to=[to_email])
    if email.send():
        messages.success(request, f'Estimado <b>{user.username}</b>, por favor ve a su bandeja de entrada del correo electrónico \
                     <b>{to_email}</b> y haz click en el enlace de activación recibido para confirmar y completar el registro. <b>Nota:</b> Revisa tu carpeta de spam.')
    else:
        messages.error(request, f'Problema al enviar el correo a {to_email}, verifique si esta correctamente escrito.')

# Create your views here.
@user_not_authenticated(redirect_url='homepage')
def register(request):
    #if request.user.is_authenticated:
    #    return redirect('homepage')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request,user,form.cleaned_data.get('email'))
            #login(request, user)
            #messages.success(request,f'Cuenta registrada con éxito.')
            return redirect('homepage')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
    else:
        form = UserRegisterForm()

    return render(request,'user/auth/register.html',context={'form':form,'title':'Registro'})

@login_required(login_url='login')
def custom_logout(request):
    logout(request)
    messages.info(request,'Has cerrado sesión exitosamente!')
    return redirect('homepage')


@user_not_authenticated(redirect_url='homepage')
def custom_login(request):
    #if request.user.is_authenticated:
    #    return redirect('homepage')
    if request.method == 'POST':
        form = UserLoginForm(request=request, data= request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request,f'Hola <b>{user.username}</b>. Has iniciado sesión!')
                return redirect('homepage')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'Este campo es obligatorio.':
                    messages.error(request,'No ha pasado la prueba de reCAPTCHA')
                    continue
                messages.error(request,error)

    form = UserLoginForm()
    return render(request,'user/auth/login.html',context={'form':form,'title':'Inicio de sesión'})


def profile(request,username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request,f'<b>{user_form.username}</b>. Tu perfil ha sido actualizado!')
            return redirect('profile',user_form.username)
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

    user = get_user_model().objects.filter(username=username).first()

    if user :
        form = UserUpdateForm(instance=user)
        return render(request=request,template_name='user/auth/profile.html',context={'form':form,'title':'Profile'})
    return redirect('homepage')

@login_required(login_url='login')
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu contraseña ha sido cambiada.")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'user/auth/password_reset_confirm.html', {'form': form})

@user_not_authenticated(redirect_url='homepage')
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Solicitud de restablecimiento de contraseña"
                message = render_to_string("user/auth/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Contraseña restablecida enviada</h2><hr>
                        <p>
                        Te hemos enviado por correo electrónico las instrucciones para establecer tu contraseña, si existe una cuenta asociada al correo electrónico que ingresaste.
                        Deberías recibir pronto dichas instrucciones.<br>Si no recibes un correo electrónico, por favor asegúrate de haber ingresado la dirección con la que te registraste
                        y revisa tu carpeta de correo no deseado (spam).
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problema al enviar el correo electrónico de restablecimiento de contraseña, <b>PROBLEMA DEL SERVIDOR</b>")

            return redirect('homepage')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'Este campo es obligatorio.':
                messages.error(request,'No ha pasado la prueba de reCAPTCHA')
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="user/auth/password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Tu contraseña ha sido establecida. Ahora puedes <b>iniciar sesión</b>.")
                return redirect('homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'user/auth/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "El enlace ha caducado")

    messages.error(request, 'Algo salió mal, redirigiendo de vuelta a la página de inicio')
    return redirect("homepage")
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from .forms import SignUpForm, CustomUserCreationForm
from django.views.generic.detail import DetailView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from .models import User
from django.http import HttpResponseBadRequest
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages

User = get_user_model() 

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send email confirmation
            current_site = get_current_site(request)
            subject = 'Activer votre compte'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.info(request, "Un lien d\'activation a été envoyé à votre adresse mail. Veuillez vérifier votre boîte de réception et cliquer sur le lien d\'activation pour activer votre compte.")
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/')
    else:
        return HttpResponseBadRequest("Le lien d'activation est invalide")
    

def account_activation_complete(request):
    return render(request, 'registration/account_activation_complete.html')


class UserView(DetailView):
    model = User
    template_name = 'registration/profile.html'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return '/' 
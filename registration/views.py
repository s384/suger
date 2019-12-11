from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import FormView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from .forms import EmailForm

# Create your views here.

class ActivationForm(FormView):
    template_name = 'registration/account_activation_form.html'
    form_class = EmailForm
    success_url = 'account_activation_sent'
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.email = request.POST.get('email')
        self.user = get_object_or_404(User, email=self.email)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        current_site = get_current_site(self.request)
        subject = "Activacion de cuenta en Suger"
        message = render_to_string('registration/account_activation_email.html', {
            'user': self.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user),
        })
        send_mail(
            subject,
            message,
            'suger@suger.cl',
            [self.email],
            fail_silently=False,
            )
        return HttpResponseRedirect(reverse_lazy(self.get_success_url()))

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.profile.first_login = True
        user.is_active = True
        user.profile.save()
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login

from .forms import UserRegistrationForm


def registration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        _send_mail(user)

        return redirect('account')

    return render(request,
                  'Public/Registration/registration.html',
                  {'form': form})


def _send_mail(user):
    subject = _('Registration')
    message = render_to_string(
        'Public/Messages/registration_message.html',
        {
            'username': str(user.username),
        }
    )
    try:
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
    except Exception:
        print('SEND ERROR!')

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django_hosts.resolvers import reverse as reverse_host

from .forms import AuthenticationForm
from django.contrib.auth.models import User


def login_user(request):
    next_page = request.GET.get('next')
    if request.user.is_authenticated:
        if next_page:
            return HttpResponseRedirect(next_page)
        return redirect('account')

    initial = {'email': request.COOKIES.get('email', '')}
    form = AuthenticationForm(request.POST or None,
                              initial=initial,
                              request=request)

    if form.is_valid():
        data = form.cleaned_data
        user = None

        u = User.objects.get(email=data['email'])
        if u.check_password(data['password']):
            user = u

        if not user:
            form.add_error(None, _("Please enter a correct email and password."))
        elif user.is_active:
            login(request, user)

            if next_page and is_safe_url(next_page, allowed_hosts=settings.ALLOWED_HOSTS):
                redirect_url = next_page
            else:
                redirect_url = reverse_host('account', host='public')
            response = HttpResponseRedirect(redirect_url)
            response.set_cookie('email', user.email)
            return response
        else:
            form.add_error(None, _("This account is inactive."))

    return render(request, 'Public/Home/login.html',
                  {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))

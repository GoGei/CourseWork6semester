from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django_hosts.resolvers import reverse as reverse_host
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django_hosts import reverse

from .forms import AuthenticationForm

from django.contrib.auth.models import User


def manager_login(request):
    next_page = request.GET.get('next')
    if request.user.is_authenticated:
        if next_page:
            return HttpResponseRedirect(next_page)
        return redirect('home-index')

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
        elif user.is_active and (user.is_staff or user.is_superuser):
            login(request, user)
            if next_page and is_safe_url(next_page, allowed_hosts=settings.ALLOWED_HOSTS):
                redirect_url = next_page
            else:
                redirect_url = reverse_host('home-index', host='manager')
            response = HttpResponseRedirect(redirect_url)
            response.set_cookie('email', user.email)
            return response

        elif not user.is_staff or not user.is_superuser:
            form.add_error(None, _("This account is not staff."))
        else:
            form.add_error(None, _("This account is inactive."))

    return render(request, 'Manager/Login/login.html',
                  {'form': form})


@login_required
def manager_logout(request):
    logout(request)
    return redirect(reverse('manager-login', host='manager'))

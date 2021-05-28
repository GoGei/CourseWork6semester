from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.Access.decorators import manager_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@manager_required
def user_list(request):
    qs = User.objects.filter(is_staff=False).all().order_by('-id')

    return render(request,
                  'Manager/User/user_list.html',
                  {'qs': qs})


@manager_required
def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    return render(request,
                  'Manager/User/user_details.html',
                  {'user': user})


@manager_required
def user_archive(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    messages.success(request, _('User "%s" was successfully archived') % user.username)
    return redirect(reverse('user-list'))

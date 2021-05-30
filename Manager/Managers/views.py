from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.Access.decorators import manager_required
from django.contrib.auth.models import User
from .forms import ManagerAddForm, ManagerEditForm


@manager_required
def manager_list(request):
    qs = User.objects.filter(is_staff=True).order_by('-id')

    return render(request,
                  'Manager/Manager/manager_list.html',
                  {'qs': qs})


@manager_required
def manager_add(request):
    form_body = ManagerAddForm(request.POST or None)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-list'))

    if form_body.is_valid():
        manager = form_body.save()
        messages.success(request, _('Manager "%s" profile was successfully added') % manager.email)
        return redirect(reverse('manager-list'))

    form = {'body': form_body,
            'title': _('Add manager'),
            'buttons': {'save': True, 'cancel': True}}

    return render(request,
                  'Manager/Manager/manager_add.html',
                  {'form': form})


@manager_required
def manager_edit(request, manager_id):
    manager = get_object_or_404(User, pk=manager_id)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-list'))

    form_body = ManagerEditForm(request.POST or None, instance=manager)

    if form_body.is_valid():
        manager = form_body.save()
        messages.success(request, _('Manager "%s" profile was successfully edited') % manager.email)
        return redirect(reverse('manager-list'))

    form = {'body': form_body,
            'title': _('Edit manager'),
            'buttons': {'save': True, 'cancel': True}}

    return render(request,
                  'Manager/Manager/manager_edit.html',
                  {'form': form,
                   'obj_id': manager.id})


@manager_required
def manager_details(request, manager_id):
    manager = get_object_or_404(User, pk=manager_id)

    return render(request,
                  'Manager/Manager/manager_details.html',
                  {'manager': manager})


@manager_required
def manager_delete(request, manager_id):
    manager = get_object_or_404(User, pk=manager_id)
    if manager.is_superuser:
        messages.warning(request, _('Cannot archive superuser %s!') % manager.email)
        return redirect(reverse('manager-list'))
    if manager.email == request.user.email:
        messages.warning(request, _('Cannot archive user that is currently logged in %s!') % manager.email)
        return redirect(reverse('manager-list'))
    email = manager.email
    manager.delete()
    messages.success(request, _('Manager "%s" profile was successfully deleted') % email)
    return redirect(reverse('manager-list'))

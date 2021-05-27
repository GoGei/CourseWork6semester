from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms import model_to_dict

from core.Access.decorators import manager_required
from core.Offer.models import Offer
from .forms import CreatedOfferAddForm, CreatedOfferEditForm, PickUpOfferEditForm


@manager_required
def offer_list(request, state):
    qs = Offer.objects.filter(state=state).order_by('-id')

    state_template_name_map = {
        'created': 'Manager/Offer/Created/offer_list.html',
        'pick_up': 'Manager/Offer/PickUp/offer_list.html',
        'closed': 'Manager/Offer/Closed/offer_list.html',
        'deny': 'Manager/Offer/Deny/offer_list.html',
    }
    template = state_template_name_map[state]

    return render(request,
                  template,
                  {'qs': qs})


@manager_required
def offer_add(request, state):
    state_template_name_map = {
        'created': {
            'form': CreatedOfferAddForm,
            'template': 'Manager/Offer/Created/offer_add.html'
        },
    }

    form_body = state_template_name_map[state]['form'](request.POST or None)

    if '_cancel' in request.POST:
        return redirect(reverse('offer-list', args=[state]))

    if form_body.is_valid():
        offer = form_body.save()
        offer.creator = request.user
        offer.save()
        messages.success(request, _('Offer "%s" was successfully added') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))

    form = {'body': form_body,
            'title': _('Add offer'),
            'buttons': {'save': True, 'cancel': True}}

    template = state_template_name_map[state]['template']

    return render(request,
                  template,
                  {'form': form})


@manager_required
def offer_edit(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    state_template_name_map = {
        'created': {
            'form': CreatedOfferEditForm,
            'template': 'Manager/Offer/Created/offer_edit.html'
        },
        'pick_up': {
            'form': PickUpOfferEditForm,
            'template': 'Manager/Offer/PickUp/offer_edit.html'
        }
    }

    if '_cancel' in request.POST:
        return redirect(reverse('offer-list', args=[state]))

    initial = model_to_dict(offer)
    initial['clients'] = [item.id for item in offer.clients.all()]
    form_body = state_template_name_map[state]['form'](request.POST or None, instance=offer, initial=initial)

    if form_body.is_valid():
        offer = form_body.save()
        messages.success(request, _('Offer "%s" was successfully edited') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))

    form = {'body': form_body,
            'title': _('Edit offer'),
            'buttons': {'save': True, 'cancel': True}}

    template = state_template_name_map[state]['template']
    return render(request,
                  template,
                  {'form': form,
                   'obj_id': offer.id})


@manager_required
def offer_details(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    state_template_name_map = {
        'created': 'Manager/Offer/Created/offer_details.html',
        'pick_up': 'Manager/Offer/PickUp/offer_details.html',
        'closed': 'Manager/Offer/Closed/offer_details.html',
        'deny': 'Manager/Offer/Deny/offer_details.html',
    }
    template = state_template_name_map[state]
    return render(request,
                  template,
                  {'offer': offer})


@manager_required
def offer_archive(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.archive(request.user)
    offer.save()
    messages.success(request, _('Offer "%s" was successfully archived') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_restore(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.archived = None
    offer.save()
    messages.success(request, _('Offer "%s" was successfully restored') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_pick_up(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.state = Offer.PICK_UP
    offer.manager = request.user
    offer.save()
    messages.success(request, _('Offer "%s" was successfully pick up') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_deny(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.state = Offer.DENY
    offer.save()
    messages.success(request, _('Offer "%s" was successfully deny') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_close(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    offer.state = Offer.CLOSED
    offer.save()
    messages.success(request, _('Offer "%s" was successfully closed') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))

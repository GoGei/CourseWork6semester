import csv

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms import model_to_dict
from django.http import HttpResponse
from core.Access.decorators import manager_required

from core.Offer.models import Offer
from core.Deal.models import Deal, DealFile
from .forms import CreatedOfferAddForm, CreatedOfferEditForm, PickUpOfferEditForm, OfferLangFormSet
from Manager.Deals.forms import DealFileAddForm


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
    lang_form_set = OfferLangFormSet(request.POST or None,
                                    request.FILES or None,
                                    prefix='offer',
                                    can_delete=False)

    if '_cancel' in request.POST:
        return redirect(reverse('offer-list', args=[state]))

    if form_body.is_valid() and lang_form_set.is_valid():
        offer = form_body.save()
        offer.creator = request.user
        lang_form_set.save(offer)
        offer.save()
        messages.success(request, _('Offer "%s" was successfully added') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))

    form = {'body': form_body,
            'title': _('Add offer'),
            'buttons': {'save': True, 'cancel': True}}

    template = state_template_name_map[state]['template']

    return render(request,
                  template,
                  {'form': form,
                   'lang_form_set': lang_form_set})


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
    lang_form_set = OfferLangFormSet(request.POST or None,
                                     request.FILES or None,
                                     prefix='offer',
                                     instance=offer, can_delete=False)

    if form_body.is_valid() and lang_form_set.is_valid():
        offer = form_body.save()
        lang_form_set.save(offer)
        messages.success(request, _('Offer "%s" was successfully edited') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))

    form = {'body': form_body,
            'title': _('Edit offer'),
            'buttons': {'save': True, 'cancel': True}}

    template = state_template_name_map[state]['template']
    return render(request,
                  template,
                  {'form': form,
                   'lang_form_set': lang_form_set,
                   'obj_id': offer.id})


@manager_required
def offer_details(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    state_template_name_map = {
        'created': 'Manager/Offer/Created/offer_details.html',
        'pick_up': 'Manager/Offer/PickUp/offer_details.html',
        'closed': 'Manager/Offer/Closed/offer_details.html',
    }
    template = state_template_name_map[state]
    if state != 'created':
        deal = get_object_or_404(Deal, offer=offer)
        return render(request,
                      template,
                      {'offer': offer,
                       'deal': deal})
    else:
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
def offer_pick_up_denied(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.archived:
        messages.warning(request, _('Offer %s archived!') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))
    offer.state = Offer.PICK_UP
    offer.manager = request.user
    offer.save()
    messages.success(request, _('Offer "%s" was successfully pick up from deny') % offer.pk)
    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_pick_up(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.archived:
        messages.warning(request, _('Offer %s archived!') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))
    offer.state = Offer.PICK_UP
    offer.manager = request.user
    offer.save()

    deal = Deal()
    deal.manager = offer.manager
    deal.offer = offer
    deal.save()

    messages.success(request, _('Offer "%s" was successfully pick up') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_deny(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.archived:
        messages.warning(request, _('Offer %s archived!') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))
    offer.state = Offer.DENY
    offer.save()
    messages.success(request, _('Offer "%s" was successfully deny') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_close(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.archived or not offer.clients.all().exists():
        messages.warning(request, _('Offer %s archived or has no clients!') % offer.pk)
        return redirect(reverse('offer-list', args=[state]))
    offer.state = Offer.CLOSED
    offer.save()
    messages.success(request, _('Offer "%s" was successfully closed') % offer.pk)

    return redirect(reverse('offer-list', args=[state]))


@manager_required
def offer_add_file(request, state, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    form_body = DealFileAddForm(request.POST or None, request.FILES or None, offer=offer)

    if '_cancel' in request.POST:
        return redirect(reverse('offer-details', args=[state, offer.id]))

    if form_body.is_valid():
        deal_file = form_body.save()
        deal_file.save()
        messages.success(request, _('Deal file "%s" was successfully added') % deal_file.pk)
        return redirect(reverse('offer-details', args=[state, offer.id]))

    form = {'body': form_body,
            'title': _('Add offer'),
            'buttons': {'save': True, 'cancel': True}}

    return render(request,
                  'Manager/Offer/PickUp/Files/offer_files_add.html',
                  {'form': form,
                   'offer': offer})


@manager_required
def offer_delete_file(request, state, file_id):
    file = get_object_or_404(DealFile, pk=file_id)
    offer = file.deal.offer
    pk = file.pk
    file.delete()
    messages.success(request, _('File "%s" was successfully deleted') % pk)

    return redirect(reverse('offer-details', args=[state, offer.id]))


def offer_export(request, state, export_to):
    if export_to == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="offers.csv"'

        writer = csv.writer(response)
        writer.writerow(['creator', 'manager', 'clients', 'address', 'price'])

        offers = Offer.objects.active().filter(state=Offer.CLOSED).all()
        for offer in offers:
            o = [str(offer.creator), str(offer.manager), ', '.join([str(client) for client in offer.clients.all()]), str(offer.address), str(offer.price)]
            writer.writerow(o)
        return response
    elif export_to == 'xls':
        pass

    messages.warning(request, _('Error when export occurred'))
    return redirect(reverse('offer-list', args=[state]))

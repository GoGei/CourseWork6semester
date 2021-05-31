from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from core.Offer.models import Offer
from core.OfferRequest.models import OfferRequest


@login_required
def account_user(request):
    user = request.user
    viewed_offers = OfferRequest.objects.active().filter(user=user, offer__state=Offer.PICK_UP).all().order_by('-created')
    closed_offers = OfferRequest.objects.active().filter(Q(offer__state=Offer.CLOSED) | Q(offer__state=Offer.DENY), user=user).all().order_by('-created')

    return render(request, 'Public/Account/account.html',
                  {'user': user,
                   'viewed_offers': viewed_offers,
                   'closed_offers': closed_offers})


@login_required
def account_add_to_viewed(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    offer_request, created = OfferRequest.objects.get_or_create(offer=offer, user=request.user)
    if offer_request.state == OfferRequest.ACCEPTED:
        messages.success(request, _('Offer is already approved'))
    elif offer_request.state == OfferRequest.VIEWED_BY_USER or \
            offer_request.state == OfferRequest.VIEWED_BY_MANAGER:
        messages.success(request, _('Offer is already added'))
    else:
        offer_request = fill_in_offer_request(offer_request, offer, request.user)
        offer_request.save()
        messages.success(request, _('Offer was added'))
    return redirect(reverse('account'))


def fill_in_offer_request(offer_request, offer, user):
    offer_request.offer = offer
    offer_request.user = user
    offer_request.state = OfferRequest.VIEWED_BY_USER
    offer_request.archived = None
    return offer_request


@login_required
def account_remove_from_viewed(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, id=offer_request_id)
    offer_request.state = OfferRequest.DECLINED
    offer_request.archive()
    offer_request.save()
    messages.success(request, _('Offer was removed'))
    return redirect(reverse('account'))


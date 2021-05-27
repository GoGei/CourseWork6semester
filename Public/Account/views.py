from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from core.Offer.models import Offer
from core.OfferRequest.models import OfferRequest


@login_required
def account_user(request):
    user = request.user
    viewed_offers = OfferRequest.objects.active().filter(user=user).all().order_by('-created')

    return render(request, 'Public/Account/account.html',
                  {'user': user,
                   'viewed_offers': viewed_offers})


@login_required
def account_add_to_viewed(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if_viewed_qs = OfferRequest.objects.filter(offer=offer, user=request.user)
    if if_viewed_qs.exists():
        messages.warning(request, _('Offer is already viewed'))
    else:
        offer_request = OfferRequest()
        offer_request.offer = offer
        offer_request.user = request.user
        offer_request.save()
        messages.success(request, _('Offer was created'))
    return redirect(reverse('account'))


@login_required
def account_remove_from_viewed(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, id=offer_request_id)
    offer_request.archive()
    offer_request.save()
    messages.success(request, _('Offer was removed'))
    return redirect(reverse('account'))


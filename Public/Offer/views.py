from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.Offer.models import Offer


@login_required
def offer_view(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request,
                  'Public/Offer/offer_view.html',
                  {'offer': offer})

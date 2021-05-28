from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from core.Access.decorators import manager_required
from django.http import JsonResponse

from core.OfferRequest.models import OfferRequest


@manager_required
def offer_request_list(request):
    qs = OfferRequest.objects.all().order_by('-id')

    return render(request,
                  'Manager/OfferRequest/offer_request_list.html',
                  {'qs': qs})


@manager_required
def offer_request_details(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, pk=offer_request_id)
    offer_request.state = OfferRequest.VIEWED_BY_MANAGER
    return render(request,
                  'Manager/OfferRequest/offer_request_details.html',
                  {'offer_request': offer_request})


@manager_required
def offer_request_approve(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, pk=offer_request_id)
    offer_request.state = OfferRequest.ACCEPTED
    offer_request.save()
    
    offer = offer_request.offer
    offer.clients.add(offer_request.user)
    messages.success(request, _('Offer "%s" was successfully accepted') % offer_request.pk)
    _send_mail(offer_request)
    return redirect(reverse('offer-request-list'))


@manager_required
def offer_request_decline(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, pk=offer_request_id)
    offer_request.state = OfferRequest.DECLINED
    offer_request.archive()
    offer_request.save()
    messages.success(request, _('Offer "%s" was successfully declined and archived') % offer_request.pk)
    _send_mail(offer_request)
    return redirect(reverse('offer-request-list'))


@manager_required
def offer_request_restore(request, offer_request_id):
    offer_request = get_object_or_404(OfferRequest, pk=offer_request_id)
    offer_request.state = OfferRequest.VIEWED_BY_MANAGER
    offer_request.archived = None
    offer_request.save()
    messages.success(request, _('Offer "%s" was successfully restored') % offer_request.pk)
    return redirect(reverse('offer-request-list'))


@manager_required
@manager_required
def offer_request_counter(request):
    qs = OfferRequest.objects.active().filter(state=OfferRequest.VIEWED_BY_USER)
    counter = qs.count()
    return JsonResponse({'success': True,
                         'counter': counter})


def _send_mail(offer_request):
    subject = _('Offer request message')
    message = render_to_string(
        'Manager/Messages/offer_request_message.html',
        {
            'user': str(offer_request.user),
            'offer': str(offer_request.offer),
            'result': str(offer_request.state),
        }
    )
    try:
        from_email = settings.EMAIL_HOST_USER
        to_list = [offer_request.user.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
    except Exception:
        print('SEND ERROR!')

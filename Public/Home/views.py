from django.shortcuts import render
from core.Offer.models import Offer


def home_index(request):
    return render(request,
                  'Public/Home/home_index.html')


def home_contacts(request):
    return render(request,
                  'Public/Home/contacts.html')


def home_offers(request):
    qs = Offer.objects.filter(state=Offer.PICK_UP).all().order_by('-created')
    return render(request,
                  'Public/Home/offers.html',
                  {'qs': qs})


def home_about(request):
    return render(request,
                  'Public/Home/about.html')

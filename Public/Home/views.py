from django.shortcuts import render
from core.Offer.models import Offer
from django.contrib.auth.models import User
from django.contrib.auth import login


def home_index(request):
    # user = User.objects.get(email='rich.290401@gmail.com')
    # login(request, user)
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

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.forms import model_to_dict

from core.Access.decorators import manager_required
from core.Deal.models import Deal


@manager_required
def deal_list(request):
    qs = Deal.objects.order_by('-id')

    return render(request,
                  'Manager/Deal/deal_list.html',
                  {'qs': qs})


@manager_required
def deal_details(request, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    return render(request,
                  'Manager/Deal/deal_details.html',
                  {'deal': deal})


@manager_required
def deal_export(request, deal_id):
    deal = get_object_or_404(Deal, pk=deal_id)
    print('export deal', deal)
    return redirect(reverse('deal-list'))

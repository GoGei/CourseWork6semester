from django.shortcuts import render, get_object_or_404

from core.Access.decorators import manager_required
from django.contrib.auth.models import User


@manager_required
def user_list(request):
    qs = User.objects.all().filter(is_staff=False).order_by('-id')

    return render(request,
                  'Manager/User/user_list.html',
                  {'table': qs})


@manager_required
def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    return render(request,
                  'Manager/User/user_details.html',
                  {'user': user})

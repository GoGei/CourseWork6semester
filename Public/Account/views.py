from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def account_user(request):
    user = request.user
    return render(request, 'Public/Account/account.html',
                  {'user': user})

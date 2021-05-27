from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login


def registration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('account')

    return render(request,
                  'Public/Registration/registration.html',
                  {'form': form})

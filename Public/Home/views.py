from django.shortcuts import render


def home_index(request):
    return render(request,
                  'Public/Home/home_index.html')

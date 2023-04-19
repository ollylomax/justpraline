from django.shortcuts import render


def index(request):
    """ Simple route to return the Index template """

    return render(request, 'home/index.html')

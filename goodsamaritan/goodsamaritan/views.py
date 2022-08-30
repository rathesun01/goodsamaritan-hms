# Author: Roche Christopher
# Created at 7:33 PM on 23/06/22

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/profile')
    else:
        return HttpResponseRedirect("/accounts/login")


@login_required
def dashboard(request):
    return render(request, 'doctors/dashboard.html')

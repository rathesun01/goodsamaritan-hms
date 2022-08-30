# Author: Roche Christopher
# Created at 10:45 AM on 08/07/22

from django.urls import path
from vitals.views import InitialFindingsCreate

urlpatterns = [
    path('add-initial-finding', InitialFindingsCreate.as_view(), name='add-initial-finding')
]
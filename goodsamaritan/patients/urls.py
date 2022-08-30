# Author: Roche Christopher
# Created at 2:03 PM on 25/06/22

from django.urls import path
from patients.views import AdmittedPatients, AllPatients, AddNewPatient, AdmitExistingPatient, AdmitNewPatient,\
    PatientDetailView, DischargePatientCreateView, UpdatePatient, AdmissionDetailView, DischargePatientDetailView, \
    AdmissionDetailUpdateView

urlpatterns = [
    path('admitted-patients', AdmittedPatients.as_view(), name='admitted-patients'),
    path('all-patients', AllPatients.as_view(), name='all-patients'),
    path('admit-existing-patient', AdmitExistingPatient.as_view(), name='admit-existing-patient'),
    path('admit-new-patient', AdmitNewPatient.as_view(), name='admit-new-patient'),
    path('add-new-patient', AddNewPatient.as_view(), name='add-new-patient'),
    path('update-patient/<pk>', UpdatePatient.as_view(), name='update-patient'),
    path('patient/<pk>', PatientDetailView.as_view(), name='patient-detail-view'),
    path('discharge-patient', DischargePatientCreateView.as_view(), name='discharge-patient'),
    path('discharge-details/<pk>', DischargePatientDetailView.as_view(), name='discharge-detail-view'),
    path('admission/<pk>', AdmissionDetailView.as_view(), name='admission-detail-view'),
    path('update-admission/<pk>', AdmissionDetailUpdateView.as_view(), name='update-admission-detail')
]
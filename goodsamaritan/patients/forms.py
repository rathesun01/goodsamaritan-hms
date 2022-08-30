# Author: Roche Christopher
# Created at 2:23 PM on 25/06/22

from django import forms
from patients.models import PatientDetail, AdmissionDetail, CaseSheet, Sickness, ProblemsAndDiagnosis, DischargeDetail
import datetime


class NewPatientForm(forms.ModelForm):

    date_of_birth = forms.DateField(widget=forms.DateInput)
    address = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = PatientDetail
        fields = ('patient_name', 'gender', 'date_of_birth', 'address', 'contact_number', 'email', 'qualification',
                  'occupation')


class AdmitExistingPatientForm(forms.ModelForm):

    class Meta:
        model = AdmissionDetail
        fields = ('date_of_admission', 'patient')


class CaseSheetForm(forms.ModelForm):
    medical_history = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = CaseSheet
        fields = ('medical_history', )


class SicknessForm(forms.ModelForm):
    problem = forms.CharField(widget=forms.Textarea())
    symptoms = forms.CharField(widget=forms.Textarea())
    duration = forms.IntegerField()

    class Meta:
        model = Sickness
        fields = ('problem', 'symptoms', 'duration', 'duration_type')


class ProblemsAndDiagnosisForm(forms.ModelForm):

    problem = forms.CharField(widget=forms.Textarea())
    diagnosis = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = ProblemsAndDiagnosis
        fields = ('problem', 'diagnosis')


class DischargeDetailForm(forms.ModelForm):

    date_of_discharge = forms.DateField(widget=forms.DateInput(), required=True, initial=datetime.date.today)
    brief_summary = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = DischargeDetail
        fields = ('date_of_discharge', 'brief_summary')

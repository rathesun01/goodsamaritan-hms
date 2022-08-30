from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django import forms
from django.http import HttpResponseRedirect, HttpResponseBadRequest

import logging

from patients.models import AdmissionDetail

from vitals.models import InitialFindings, EmotionAnalysisAssessment, BodyMindWellness, DailyRoutineVitalFindings, \
    BloodGlucose, Thyroid, Electrolytes, RenalFunctionTest, LiverFunctionTest, LipidProfile, Vitamin

from vitals.forms import InitialFindingsCreateForm, BloodGlucoseCreateForm, ThyroidForm, RenalFunctionTestForm, \
    LiverFunctionTestForm, ElectrolyteForm, LipidProfileForm, VitaminForm

logger = logging.getLogger(__name__)

# Create your views here.


class InitialFindingsCreate(CreateView):

    template_name = 'vitals/intial_findings_form.html'
    model = InitialFindings
    form_class = InitialFindingsCreateForm

    def post(self, request):

        # get admission details
        admission_id = request.GET.get('admission_id')
        logger.debug(f'The admission id is {admission_id}')
        if admission_id is None:
            return HttpResponseBadRequest()

        data = request.POST
        initial_findings = InitialFindings(data)
        logger.debug(f'The initial post data is {data}')

        initial_findings = InitialFindingsCreateForm(data)
        if initial_findings.is_valid():
            initial_findings: InitialFindings = initial_findings.save(commit=False)
            # save admission detail
            admission_detail: AdmissionDetail = AdmissionDetail.objects.get(id=admission_id)
            initial_findings.admission_detail = admission_detail

            # save all the data in their separate models first and then use that object as foreign key in initialfindings
            # model

            # save blood glucose
            blood_glucose = BloodGlucoseCreateForm(data)
            if blood_glucose.is_valid():
                blood_glucose: BloodGlucose = blood_glucose.save(commit=False)
                blood_glucose.save()

            # save thyroid
            thyroid = ThyroidForm(data)
            if thyroid.is_valid():
                thyroid: Thyroid = thyroid.save(commit=False)
                thyroid.save()

            # save rft
            rft = RenalFunctionTestForm(data)
            if rft.is_valid():
                rft: RenalFunctionTest = rft.save(commit=False)
                rft.save()

            # save lft
            lft = LiverFunctionTestForm(data)
            if lft.is_valid():
                lft: LiverFunctionTest = lft.save(commit=False)
                lft.save()

            # save electrolytes
            electrolytes = ElectrolyteForm(data)
            if electrolytes.is_valid():
                electrolytes: Electrolytes = electrolytes.save(commit=False)
                electrolytes.save()

            # save lipid profile
            lipid_profile = LipidProfileForm(data)
            if lipid_profile.is_valid():
                lipid_profile: LipidProfile = lipid_profile.save(commit=False)
                lipid_profile.save()

            # save vitamin
            vitamin = VitaminForm(data)
            if vitamin.is_valid():
                vitamin: Vitamin = vitamin.save(commit=False)
                vitamin.save()

            # link vitals objects to initial findings
            initial_findings.blood_glucose = blood_glucose
            initial_findings.thyroid = thyroid
            initial_findings.rft = rft
            initial_findings.lft = lft
            initial_findings.electrolytes = electrolytes
            initial_findings.lipid_profile = lipid_profile
            initial_findings.vitamin = vitamin

            # save initital findings
            initial_findings.save()

            return HttpResponseRedirect(f'/patients/patient/{admission_detail.patient.id}')
        else:
            return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super(InitialFindingsCreate, self).get_context_data()
        # add admission details
        admission_id = self.request.GET.get('admission_id')
        admission_detail: AdmissionDetail = AdmissionDetail.objects.get(id=admission_id)
        context['admission_detail'] = admission_detail

        context['blood_glucose_form'] = BloodGlucoseCreateForm()
        context['thyroid_form'] = ThyroidForm()
        context['rft_form'] = RenalFunctionTestForm()
        context['lft_form'] = LiverFunctionTestForm()
        context['electrolyte_form'] = ElectrolyteForm()
        context['lipidprofile_form'] = LipidProfileForm()
        context['vitamin_form'] = VitaminForm()
        return context

    def get_form(self, form_class=None):

        form = super(InitialFindingsCreate, self).get_form()
        form.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        return form


class InitialFindingsUpdate(UpdateView):
    pass


class DailyRoutineVitalsCreateView(CreateView):
    pass


class DailyRoutineVitalsUpdateView(UpdateView):
    pass



from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from patients.models import PatientDetail, AdmissionDetail, DischargeDetail, CaseSheet, Sickness, ProblemsAndDiagnosis
from doctors.models import DoctorDetail

from django.http import HttpResponseRedirect
from django import forms
from patients.forms import NewPatientForm, AdmitExistingPatientForm, SicknessForm, CaseSheetForm, DischargeDetailForm, \
    ProblemsAndDiagnosisForm
from phone_field import PhoneFormField, PhoneWidget

import logging

logger = logging.getLogger(__name__)

# Create your views here.


class AdmittedPatients(ListView):
    model = PatientDetail
    template_name = 'patients/admitted_patients.html'

    def get_queryset(self):
        admitted_patients = PatientDetail.get_currently_admitted_patients()
        return admitted_patients


class AllPatients(ListView):
    model = PatientDetail
    template_name = 'patients/all_patients.html'


class AdmitNewPatient(ListView):
    pass


class AdmitExistingPatient(CreateView):
    template_name = 'patients/admit_existing_patient.html'
    model = AdmissionDetail
    fields = ('patient', 'date_of_admission')

    def get_form(self, form_class=None):

        form = super(AdmitExistingPatient, self).get_form()
        form.fields['date_of_admission'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['patient'].queryset = PatientDetail.get_unadmitted_patients()
        logger.debug(f'the fields for admit existing patients are {form.fields}')
        patient_id = self.request.GET.get('id')
        if patient_id is not None:
            form.fields['patient'].initial = patient_id

        return form

    def get_queryset(self):
        queryset = super(AdmitExistingPatient, self).get_queryset()
        logger.debug(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdmitExistingPatient, self).get_context_data()
        sickness_formset_factory = forms.formset_factory(SicknessForm)
        context['sickness_formset'] = sickness_formset_factory()
        context['casesheet_form'] = CaseSheetForm
        return context

    def post(self, request):
        data = request.POST
        admit_form = AdmitExistingPatientForm(data)
        if admit_form.is_valid():
            admission: AdmissionDetail = admit_form.save(commit=False)
            logger.debug(admission)
            logger.debug(f'the user is {request.user} and the doctor is {request.user.doctor_detail}')
            logger.debug(DoctorDetail.objects.filter(auth_user=request.user))
            admission.doctor = DoctorDetail.objects.get(auth_user=request.user)
            admission.save()

            # create a case sheet
            case_sheet_form = CaseSheetForm(data)
            if case_sheet_form.is_valid():
                case_sheet: CaseSheet = case_sheet_form.save(commit=False)
                case_sheet.admission_detail = admission
                if case_sheet.date is None:
                    logger.debug("case sheet date is none. so setting admission's date")
                    case_sheet.date = admission.date_of_admission
                case_sheet.save()

                # save the sicknesses
                sickness_formset_factory = forms.formset_factory(SicknessForm)
                sicknesses = sickness_formset_factory(data)
                if sicknesses.is_valid():
                    for _sickness in sicknesses:
                        sickness_form = SicknessForm(_sickness.cleaned_data)
                        sickness: Sickness = sickness_form.save(commit=False)
                        sickness.case_sheet = case_sheet
                        sickness.save()
                        logger.debug(f'saved sickness {sickness} with case sheet {case_sheet}')
            return HttpResponseRedirect('/patients/admitted-patients')


class AdmissionDetailView(DetailView):
    model = AdmissionDetail
    template_name = 'patients/admission_detail.html'

    def get_context_data(self, **kwargs):

        context = super(AdmissionDetailView, self).get_context_data()
        current_admission_detail: AdmissionDetail = kwargs.get('object')
        context['current_admission_detail'] = current_admission_detail
        case_sheet: CaseSheet = current_admission_detail.get_case_sheet()
        context['case_sheet'] = case_sheet
        sicknesses = case_sheet.get_sicknesses()
        context['sicknesses'] = sicknesses

        return context


class AdmissionDetailUpdateView(UpdateView):

    model = AdmissionDetail
    template_name = 'patients/update_admission.html'
    fields = ('date_of_admission',)

    def get_form(self, form_class=None):
        form = super(AdmissionDetailUpdateView, self).get_form()
        form.fields['date_of_admission'].widget = forms.DateInput(attrs={'type': 'date'})

        return form

    def get_context_data(self, **kwargs):

        context = super(AdmissionDetailUpdateView, self).get_context_data()
        logger.debug(f'the kwargs in admission detail update view is {kwargs} and {self.object}')
        case_sheet: CaseSheet = self.object.get_case_sheet()
        context['casesheet_form'] = CaseSheetForm(instance=case_sheet)
        sickness_formset_factory = forms.formset_factory(SicknessForm)
        sickness_formset_data = sickness_formset_factory(data=case_sheet.get_sicknesses())
        # logger.debug(f'sicknesses formset data is {sicknesses_formset_data}')
        context['sickness_formset'] = sickness_formset_data

        return context


class AddNewPatient(CreateView):
    template_name = 'patients/add_new_patient.html'

    model = PatientDetail
    fields = ('patient_name', 'gender', 'date_of_birth', 'address', 'contact_number', 'email', 'qualification',
              'occupation')

    def get_form(self):
        form = super(AddNewPatient, self).get_form()
        form.fields['address'].widget = forms.Textarea()
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={"type": 'date'})
        form.fields['contact_number'].widget = PhoneWidget()
        return form

    def post(self, request):
        new_patient_form = NewPatientForm(self.request.POST)
        if new_patient_form.is_valid():
            logger.debug(f"New patient data {new_patient_form.cleaned_data}")
            patient_detail: PatientDetail = new_patient_form.save(commit=False)
            patient_detail.save()
            return HttpResponseRedirect('/patients/all-patients')
        else:
            print(f'not valid {new_patient_form.errors}')


class UpdatePatient(UpdateView):

    model = PatientDetail
    fields = ('patient_name', 'gender', 'date_of_birth', 'address', 'contact_number', 'email', 'qualification',
              'occupation')
    template_name = 'patients/update_patient_details.html'

    def post(self, request, **kwargs):
        logger.debug(f'The keyword args are {kwargs}')
        return HttpResponseRedirect(f'/patients/patient/{kwargs.get("pk")}')


class PatientDetailView(DetailView):
    model = PatientDetail
    template_name = 'patients/patient.html'

    # def get_queryset(self):
    #     patient = super(PatientDetailView, self).get_queryset()
    #     return patient

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data()
        patient: PatientDetail = kwargs.get('object')
        logger.debug(f'patient to be viewed is {patient}')
        if patient.is_admitted():
            current_admission_detail: AdmissionDetail = self.object.get_current_admission_detail()
            logger.debug(f'current admission detail {self.object.get_current_admission_detail()}')
            context['current_admission_detail'] = current_admission_detail
            case_sheet: CaseSheet = current_admission_detail.get_case_sheet()
            context['case_sheet'] = case_sheet
            sicknesses = case_sheet.get_sicknesses()
            context['sicknesses'] = sicknesses
            initial_findings = current_admission_detail.get_initial_findings()
            logger.debug(f'initial findings {initial_findings}')
            context['initial_findings'] = initial_findings

        previous_admission_details = patient.get_previous_admission_details()
        if previous_admission_details is not None:
            admission_data_to_display = []

            for admission_details in previous_admission_details:
                logger.debug(admission_details)
                logger.debug(admission_details.discharge_detail)
                admission_data_to_display.append({
                    'date_of_admission': admission_details.date_of_admission,
                    'date_of_discharge': admission_details.discharge_detail.date_of_discharge,
                    'admission_id': admission_details.id,
                    'discharge_id': admission_details.discharge_detail.id
                })
            context['previous_admissions'] = admission_data_to_display

        return context


class DischargePatientCreateView(CreateView):

    template_name = 'patients/discharge_form.html'
    model = DischargeDetail
    form_class = DischargeDetailForm

    def get_form(self, form_class=None):

        form = super(DischargePatientCreateView, self).get_form()
        form.fields['date_of_discharge'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

    def get_queryset(self):
        queryset = super(DischargePatientCreateView, self).get_queryset()
        logger.debug(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DischargePatientCreateView, self).get_context_data()
        pnd_formset_factory = forms.formset_factory(ProblemsAndDiagnosisForm)
        context['pnd_formset'] = pnd_formset_factory()

        admission_id = self.request.GET.get('admission_id')
        admission_detail: AdmissionDetail = AdmissionDetail.objects.get(id=admission_id)
        context['admission_detail'] = admission_detail
        context['patient_details'] = admission_detail.patient

        return context

    def post(self, request):
        data = request.POST
        discharge_form = DischargeDetailForm(data)
        logger.debug(f'The discharge post is {data}')

        if discharge_form.is_valid():
            discharge_detail: DischargeDetail = discharge_form.save(commit=False)
            logger.debug(discharge_detail)
            logger.debug(f'the user is {request.user} and the doctor is {request.user.doctor_detail}')
            logger.debug(DoctorDetail.objects.filter(auth_user=request.user))
            admission_id = request.GET.get('admission_id')
            logger.debug(f'admission is {admission_id}')
            discharge_detail.admission_detail = AdmissionDetail.objects.get(id=admission_id)
            discharge_detail.save()

            # create problems and diagnosis record
            pnd_formset_factory = forms.formset_factory(ProblemsAndDiagnosisForm)
            pnds = pnd_formset_factory(data)
            if pnds.is_valid():
                for _pnd in pnds:
                    pnd_form = ProblemsAndDiagnosisForm(_pnd.cleaned_data)
                    pnd: ProblemsAndDiagnosis = pnd_form.save(commit=False)
                    pnd.discharge_detail = discharge_detail
                    pnd.save()
                    logger.debug(f'saved pnd {pnd} with discharge detail {discharge_detail}')
            return HttpResponseRedirect(f'/patients/patient/{discharge_detail.admission_detail.patient.id}')


class DischargePatientDetailView(DetailView):
    model = DischargeDetail
    template_name = 'patients/discharge_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DischargePatientDetailView, self).get_context_data()
        discharge_detail: DischargeDetail = kwargs.get('object')
        pnd: ProblemsAndDiagnosis = discharge_detail.get_problems_and_diagnosis()
        context['pnds'] = pnd

        return context



# class AddNewPatient(FormView):
#     template_name = 'patients/add_new_patient.html'
#     form_class = NewPatientForm
#     success_url = HttpResponseRedirect('/patients/all-patients')
#
#     def form_valid(self, form):
#         # This method is called when a post request is made to this url
#         print("Post new patient")
#         print(self.request)
#         return HttpResponseRedirect('dashboard')



from django.db import models
from doctors.models import DoctorDetail
from phone_field import PhoneField
import datetime

import logging

logger = logging.getLogger(__name__)

# Create your models here.


class PatientDetail(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female")
    ]

    patient_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=1024)
    contact_number = PhoneField(blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    qualification = models.CharField(max_length=32, blank=True)
    occupation = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.patient_name

    def get_current_admission_detail(self):
        queryset = AdmissionDetail.objects.filter(patient=self).filter(discharge_detail=None)
        logger.debug(f'current admission details for user {self.patient_name} is {queryset}')
        if len(queryset) != 0:
            logger.debug('inside')
            return queryset[0]
        return None

    def is_admitted(self):
        if self.get_current_admission_detail() is None:
            return False
        return True

    def get_previous_admission_details(self):
        queryset = AdmissionDetail.objects.filter(patient=self).exclude(discharge_detail=None)
        logger.debug(f'previous admission details for user {self.patient_name} are {queryset}')
        if len(queryset) != 0:
            return queryset
        return None

    @staticmethod
    def get_currently_admitted_patients():
        # filter the patients that are admitted by this doctor
        # filter the admission details that do not have a corresponding discharge data.
        admission_details = AdmissionDetail.objects.filter(discharge_detail=None)
        admitted_patients = PatientDetail.objects.filter(admission_detail__in=admission_details)
        logger.debug(f'currently admitted patients are {admission_details}')
        return admitted_patients

    @staticmethod
    def get_unadmitted_patients():
        unadmitted_patients = PatientDetail.objects.exclude(id__in=PatientDetail.get_currently_admitted_patients())
        logger.debug(f'unadmitted patients are {unadmitted_patients}')
        return unadmitted_patients


class AdmissionDetail(models.Model):
    date_of_admission = models.DateField(default=datetime.date.today)
    doctor = models.ForeignKey(DoctorDetail, on_delete=models.DO_NOTHING, related_name='admission_detail')
    patient = models.ForeignKey(PatientDetail, on_delete=models.DO_NOTHING, related_name='admission_detail')

    def get_case_sheet(self):
        return CaseSheet.objects.get(admission_detail=self)

    def get_initial_findings(self):
        from vitals.models import InitialFindings
        initial_findings = None
        try:
            initial_findings = InitialFindings.objects.get(admission_detail=self)
        except InitialFindings.DoesNotExist:
            pass
        return initial_findings

class CaseSheet(models.Model):
    date = models.DateField()
    medical_history = models.CharField(max_length=2**16)
    admission_detail = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING,
                                            related_name='case_sheet', null=False, blank=False)

    def get_sicknesses(self):
        return Sickness.objects.filter(case_sheet=self)


class Sickness(models.Model):
    """
        This model contains the problems, symptoms and duration of sickness
    """
    DAYS = "DAYS"
    WEEKS = "WEEKS"
    MONTHS = "MONTHS"
    YEARS = "YEARS"
    DURATION_CHOICES = [
        (DAYS, "Days"),
        (WEEKS, "Weeks"),
        (MONTHS, "Months"),
        (YEARS, "Years")
    ]

    problem = models.CharField(max_length=2**14, blank=False)
    symptoms = models.CharField(max_length=2**14, blank=False)
    duration = models.IntegerField()
    # TODO: Add the allowed values like days, weeks, months and years
    duration_type = models.CharField(max_length=8, choices=DURATION_CHOICES)
    case_sheet = models.ForeignKey(CaseSheet, on_delete=models.DO_NOTHING)


class DischargeDetail(models.Model):
    date_of_discharge = models.DateField(default=datetime.date.today)
    admission_detail = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING, related_name='discharge_detail')
    brief_summary = models.CharField(max_length=2**15)

    def get_problems_and_diagnosis(self):
        return ProblemsAndDiagnosis.objects.filter(discharge_detail=self)


class ProblemsAndDiagnosis(models.Model):
    """
    This model is used in DischargeDetail model
    """
    problem = models.CharField(max_length=2**4)
    diagnosis = models.CharField(max_length=2**14)
    discharge_detail = models.ForeignKey(DischargeDetail, on_delete=models.DO_NOTHING)

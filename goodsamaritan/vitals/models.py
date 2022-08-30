from django.db import models
import datetime

from patients.models import AdmissionDetail

# Create your models here.


class BloodGlucose(models.Model):
    fbs = models.IntegerField()
    ppbs = models.IntegerField()
    rbs = models.IntegerField()
    hba1c = models.IntegerField()


class BloodPressure(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()


class Vitamin(models.Model):
    vitamin_b = models.IntegerField()
    vitamin_c = models.IntegerField()
    vitamin_d3 = models.IntegerField()


class LipidProfile(models.Model):
    hdl = models.IntegerField()
    ldl = models.IntegerField()
    tgld = models.IntegerField()
    total = models.IntegerField()


class Electrolytes(models.Model):
    sodium = models.IntegerField()
    potassium = models.IntegerField()


class LiverFunctionTest(models.Model):
    ast = models.IntegerField()
    alt = models.IntegerField()
    sgot = models.IntegerField()
    sgpt = models.IntegerField()


class RenalFunctionTest(models.Model):
    urea = models.IntegerField()
    s_creatinine = models.IntegerField()
    uric_acid = models.IntegerField()


class OrganFunctionTest(models.Model):
    organ = models.CharField(max_length=64)
    value = models.IntegerField()


class EnergyFunctionTest(models.Model):
    # ENERGY_PARAMS = [
    #     ("HEAT", "Heat"),
    #     ("COLD", "Cold"),
    #     ("HUMIDITY", "Humidity"),
    #     ("WIND", "Wind"),
    #     ("DRYNESS", "Dryness")
    # ]
    # parameter = models.CharField(max_length=16, choices=ENERGY_PARAMS)
    # value = models.IntegerField()

    heat = models.IntegerField()
    cold = models.IntegerField()
    humidity = models.IntegerField()
    wind = models.IntegerField()
    dryness = models.IntegerField()


class ThoughtAnalysisAssessment(models.Model):
    straight_thought = models.IntegerField()
    spiral_thought = models.IntegerField()
    knotted_thought = models.IntegerField()
    multiple_thought = models.IntegerField()
    dip_thought = models.IntegerField()


class EmotionAnalysisAssessment(models.Model):
    muscle_movement = models.IntegerField()
    assimilation = models.IntegerField()
    restlessness = models.IntegerField()
    elimination = models.IntegerField()


class Tridosha(models.Model):
    vata = models.IntegerField()
    pita = models.IntegerField()
    kapha = models.IntegerField()


class PanchaBoothas(models.Model):
    fire = models.IntegerField()
    water = models.IntegerField()
    air = models.IntegerField()
    earth = models.IntegerField()
    akash = models.IntegerField()


class OrganEnergyBalance(models.Model):
    organ = models.CharField(max_length=32)
    balance = models.BooleanField()  # True -> tonification and False -> sedation


class Thyroid(models.Model):
    t3 = models.IntegerField()
    t4 = models.IntegerField()
    tsh = models.IntegerField()


class InitialFindings(models.Model):
    """
    This model contains the data that is taken initially when the patient is admitted and data that is brought
    by them
    """
    date = models.DateField(default=datetime.date.today)
    hemoglobin = models.IntegerField()
    wbc = models.IntegerField()
    platelets = models.IntegerField()
    blood_glucose = models.OneToOneField(BloodGlucose, on_delete=models.DO_NOTHING)
    thyroid = models.OneToOneField(Thyroid, on_delete=models.DO_NOTHING)
    rft = models.OneToOneField(RenalFunctionTest, on_delete=models.DO_NOTHING)
    lft = models.OneToOneField(LiverFunctionTest, on_delete=models.DO_NOTHING)
    electrolytes = models.OneToOneField(Electrolytes, on_delete=models.DO_NOTHING)
    lipid_profile = models.OneToOneField(LipidProfile, on_delete=models.DO_NOTHING)
    vitamin = models.OneToOneField(Vitamin, on_delete=models.DO_NOTHING)
    admission_detail = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING, related_name='initial_findings')


class DailyRoutineVitalFindings(models.Model):
    date = models.DateField(default=datetime.date.today)
    oxygen_level = models.IntegerField()
    pulse = models.IntegerField()
    blood_pressure = models.ForeignKey(BloodPressure, on_delete=models.DO_NOTHING)
    blood_glucose = models.ForeignKey(BloodGlucose, on_delete=models.DO_NOTHING)
    temperature = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    admission_details = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING)


class PulseDiagnosisInvestigations(models.Model):
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField()
    blood_pressure = models.ForeignKey(BloodPressure, on_delete=models.DO_NOTHING)
    blood_sugar = models.ForeignKey(BloodGlucose, on_delete=models.DO_NOTHING)
    oxygen = models.IntegerField()
    pulse = models.IntegerField()
    rr_interval = models.IntegerField()
    rr_interval_sec = models.IntegerField()
    panchaboothas = models.ForeignKey(PanchaBoothas, on_delete=models.DO_NOTHING)
    tridosha = models.ForeignKey(Tridosha, on_delete=models.DO_NOTHING)
    admission_details = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING)


class BodyMindWellness(models.Model):
    date = models.DateField(default=datetime.date.today)
    thought_analysis = models.ForeignKey(ThoughtAnalysisAssessment, on_delete=models.DO_NOTHING)
    emotion_analysis = models.ForeignKey(EmotionAnalysisAssessment, on_delete=models.DO_NOTHING)
    organ_energy_balance = models.ForeignKey(OrganEnergyBalance, on_delete=models.DO_NOTHING)
    admission_details = models.OneToOneField(AdmissionDetail, on_delete=models.DO_NOTHING)





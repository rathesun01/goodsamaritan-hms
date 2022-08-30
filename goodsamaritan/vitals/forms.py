# Author: Roche Christopher
# Created at 10:59 AM on 08/07/22

from django.forms.models import ModelForm
from django.forms import inlineformset_factory
from django import forms

import datetime

from vitals.models import BloodGlucose, Thyroid, RenalFunctionTest, LiverFunctionTest, Electrolytes, \
        EnergyFunctionTest, InitialFindings, LipidProfile, Vitamin


class BloodGlucoseCreateForm(ModelForm):

    class Meta:
        model = BloodGlucose
        fields = '__all__'


class ThyroidForm(ModelForm):

    class Meta:
        model = Thyroid
        fields = '__all__'


class RenalFunctionTestForm(ModelForm):

    class Meta:
        model = RenalFunctionTest
        fields = '__all__'


class LiverFunctionTestForm(ModelForm):

    class Meta:
        model = LiverFunctionTest
        fields = '__all__'


class ElectrolyteForm(ModelForm):

    class Meta:
        model = Electrolytes
        fields = '__all__'


class LipidProfileForm(ModelForm):

    class Meta:
        model = LipidProfile
        fields = '__all__'


class VitaminForm(ModelForm):

    class Meta:
        model = Vitamin
        fields = '__all__'


class InitialFindingsCreateForm(ModelForm):

    class Meta:
        model = InitialFindings
        fields = ('date', 'hemoglobin', 'wbc', 'platelets')




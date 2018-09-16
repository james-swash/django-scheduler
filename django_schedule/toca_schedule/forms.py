from django import forms
from . import models


class CreateSchedule(forms.ModelForm):
    class Meta:
        model = models.Schedule
        fields = ['job', 'action_id', 'scheduled']
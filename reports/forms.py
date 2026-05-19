from django.forms import ModelForm
from .models import Report

class ReportForm(ModelForm):

    class Meta:
        model = Report
        fields = [
            'age',
            'weight',
            'gender',
            'bp',
            'temperature',
            'diagnosis',
            'prescription',
            'notes',
            'report_file'
        ]
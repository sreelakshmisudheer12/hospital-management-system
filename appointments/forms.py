from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):

    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'id_appointment_date'
            }
        )
    )

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'reason']
from django import forms

from .models import Doctor
from appointments.models import Appointment

class DoctorUpdateForm(forms.ModelForm):

    class Meta:

        model = Doctor

        fields = [

            'doctor_id',
            'photo',
            'specialization',
            'department',
            'experience',
            'contact',
            'consultation_fee',
            'bio'

        ]

        widgets = {

            'doctor_id': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'specialization': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'experience': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'contact': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'consultation_fee': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'bio': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control'
                }
            ),

        }


class DoctorForm(forms.ModelForm):

    class Meta:

        model = Doctor

        fields = [

            'user',
            'doctor_id',
            'photo',
            'specialization',
            'department',
            'experience',
            'contact',
            'consultation_fee',
            'bio',
            'approved'

        ]
class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = [
            'appointment_date',
            'reason'
        ]

        widgets = {
            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'form-control'
                }
            ),
        }
        
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Patient
from appointments.models import Appointment


@login_required
def patient_dashboard(request):

    patient = Patient.objects.filter(user=request.user).first()

    if not patient:
        messages.error(request, "Patient profile not found.")
        return redirect('home')

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-appointment_date')

    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments
    })
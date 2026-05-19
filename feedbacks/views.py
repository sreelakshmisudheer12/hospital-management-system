from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from doctors.models import Doctor
from patients.models import Patient

@login_required
def add_feedback(request):

    doctors = Doctor.objects.filter(approved=True)
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        if not doctor_id:
            return redirect('add_feedback')

        doctor = get_object_or_404(Doctor, id=doctor_id)

        Feedback.objects.create(
            patient=patient,
            doctor=doctor,
            message=request.POST.get('message')
        )

        return redirect('patient_dashboard')

    return render(request, 'add_feedback.html', {'doctors': doctors})


def view_feedbacks(request):

    feedbacks = Feedback.objects.all()

    return render(request, 'view_feedbacks.html', {'feedbacks': feedbacks})
@login_required
def delete_feedback(request, pk):

    feedback = get_object_or_404(
        Feedback,
        id=pk
    )

    # only feedback owner can delete
    if feedback.patient.user == request.user:

        feedback.delete()

    return redirect('view_feedbacks')
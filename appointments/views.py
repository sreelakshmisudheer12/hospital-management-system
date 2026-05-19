from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.db import transaction

from reportlab.pdfgen import canvas

from .models import Appointment
from .forms import AppointmentForm

from doctors.models import Doctor, DoctorSchedule
from patients.models import Patient
from departments.models import Department


# =========================================
# SEARCH DOCTORS
# =========================================

@login_required
def search_doctors(request):

    doctors = Doctor.objects.filter(approved=True)
    departments = Department.objects.all()

    search = request.GET.get('search')
    department_id = request.GET.get('department')

    if search:
        doctors = doctors.filter(
            Q(user__username__icontains=search)
        )

    if department_id:
        doctors = doctors.filter(
            department_id=department_id
        )

    return render(request, 'search_doctors.html', {
        'doctors': doctors,
        'departments': departments
    })


# =========================================
# BOOK APPOINTMENT
# =========================================

@login_required
@transaction.atomic
def book_appointment(request, doctor_id):

    doctor = get_object_or_404(
        Doctor,
        id=doctor_id
    )

    schedules = DoctorSchedule.objects.filter(
        doctor=doctor
    )

    # CHECK PATIENT
    try:
        patient = request.user.patient

    except Patient.DoesNotExist:
        return HttpResponse(
            "Only patients can book appointments."
        )

    if request.method == "POST":

        date = request.POST.get("date")
        reason = request.POST.get("reason")

        Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            appointment_date=date,
            reason=reason,
            status="PENDING"
        )

        messages.success(
            request,
            "Appointment booked successfully."
        )

        return redirect("appointment_success")

    return render(request, "book_appointment.html", {
        "doctor": doctor,
        "schedules": schedules
    })


# =========================================
# APPOINTMENT HISTORY
# =========================================

@login_required
def appointment_history(request):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('-created_at')

    return render(request, 'appointment_history.html', {
        'appointments': appointments
    })


# =========================================
# CANCEL APPOINTMENT
# =========================================

@login_required
def cancel_appointment(request, pk):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=pk,
        patient=patient
    )

    if appointment.status == 'COMPLETED':
        messages.error(
            request,
            "Completed appointments cannot be cancelled."
        )
        return redirect('appointment_history')

    appointment.status = 'CANCELLED'
    appointment.save()

    messages.warning(
        request,
        "Appointment cancelled."
    )

    return redirect('appointment_history')


# =========================================
# RESCHEDULE APPOINTMENT
# =========================================

@login_required
def reschedule_appointment(request, pk):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=pk,
        patient=patient
    )

    if appointment.status == 'COMPLETED':
        messages.error(
            request,
            "Completed appointments cannot be rescheduled."
        )
        return redirect('appointment_history')

    if request.method == 'POST':

        form = AppointmentForm(
            request.POST,
            instance=appointment
        )

        if form.is_valid():

            new_data = form.save(commit=False)

            appointment.appointment_date = (
                new_data.appointment_date
            )

            appointment.reason = (
                new_data.reason
            )

            appointment.token_number = None

            appointment.save()

            messages.success(
                request,
                "Appointment rescheduled successfully."
            )

            return redirect('appointment_history')

    else:

        form = AppointmentForm(
            instance=appointment
        )

    return render(request, 'reschedule_appointment.html', {
        'form': form,
        'appointment': appointment
    })


# =========================================
# DOCTOR APPOINTMENTS
# =========================================

@login_required
def doctor_appointments(request):

    doctor = request.user.doctor

    appointments = Appointment.objects.filter(
        doctor=doctor
    )

    # SEARCH BY DATE
    search_date = request.GET.get('date')

    if search_date:
        appointments = appointments.filter(
            appointment_date=search_date
        )

    appointments = appointments.order_by(
        '-appointment_date',
        'token_number'
    )

    return render(request, 'doctor_appointments.html', {
        'appointments': appointments,
        'search_date': search_date
    })


# =========================================
# APPROVE APPOINTMENT
# =========================================

@login_required
def approve_appointment(request, pk):

    appointment = get_object_or_404(
        Appointment,
        id=pk
    )

    appointment.status = 'APPROVED'
    appointment.save()

    messages.success(
        request,
        'Appointment approved.'
    )

    return redirect('doctor_appointments')


# =========================================
# REJECT APPOINTMENT
# =========================================

@login_required
def reject_appointment(request, pk):

    appointment = get_object_or_404(
        Appointment,
        id=pk
    )

    appointment.status = 'REJECTED'
    appointment.save()

    messages.error(
        request,
        'Appointment rejected.'
    )

    return redirect('doctor_appointments')


# =========================================
# COMPLETE APPOINTMENT
# =========================================

@login_required
def complete_appointment(request, pk):

    appointment = get_object_or_404(
        Appointment,
        id=pk
    )

    if appointment.status in ['CANCELLED', 'REJECTED']:

        messages.error(
            request,
            "This appointment cannot be completed."
        )

        return redirect('doctor_appointments')

    appointment.status = 'COMPLETED'
    appointment.save()

    messages.success(
        request,
        'Appointment marked as completed.'
    )

    return redirect('doctor_appointments')


# =========================================
# DOWNLOAD PDF
# =========================================

@login_required
def download_appointment(request, pk):

    appointment = get_object_or_404(
        Appointment,
        id=pk
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="Appointment_{appointment.id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    y = 800

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, y, "MediCare Hospital")

    y -= 50

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        70,
        y,
        f"Appointment ID: {appointment.appointment_id}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Token: {appointment.token_number or 'Not Generated'}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Patient: {appointment.patient.user.username}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Doctor: {appointment.doctor.user.username}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Date: {appointment.appointment_date}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Status: {appointment.status}"
    )

    y -= 25

    pdf.drawString(
        70,
        y,
        f"Reason: {appointment.reason}"
    )

    pdf.showPage()
    pdf.save()

    return response


# =========================================
# DELETE APPOINTMENT
# =========================================

@login_required
def delete_appointment(request, pk):

    patient = get_object_or_404(
        Patient,
        user=request.user
    )

    appointment = get_object_or_404(
        Appointment,
        id=pk,
        patient=patient
    )

    if appointment.status == 'PENDING':

        messages.error(
            request,
            "Cannot delete pending appointments."
        )

        return redirect('appointment_history')

    appointment.delete()

    messages.success(
        request,
        "Appointment deleted successfully."
    )

    return redirect('appointment_history')


# =========================================
# SUCCESS PAGE
# =========================================

@login_required
def appointment_success(request):

    return render(
        request,
        "appointment_success.html"
    )
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from appointments.models import Appointment
from .models import Report
from .forms import ReportForm
from patients.models import Patient


# ✅ ADD REPORT (ONLY ONE CLEAN VERSION)
@login_required
@login_required
def add_report(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if Report.objects.filter(appointment=appointment).exists():
        messages.error(request, "Report already exists.")
        return redirect('doctor_appointments')

    if request.method == "POST":

        report_file = request.FILES.get('report_file')

        Report.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            doctor=appointment.doctor,

            age=request.POST.get('age'),
            weight=request.POST.get('weight'),
            gender=request.POST.get('gender'),
            bp=request.POST.get('bp'),
            temperature=request.POST.get('temperature'),
            diagnosis=request.POST.get('diagnosis'),
            prescription=request.POST.get('prescription'),
            notes=request.POST.get('notes'),

            report_file=report_file
        )

        messages.success(request, "Report saved successfully.")
        return redirect('doctor_dashboard')

    return render(request, 'add_report.html', {
        'appointment': appointment
    })
# ✅ VIEW REPORTS (PATIENT SIDE)
@login_required
def view_reports(request):

    patient = get_object_or_404(Patient, user=request.user)

    reports = Report.objects.filter(
        appointment__patient=patient
    ).order_by('-id')

    return render(request, 'view_reports.html', {
        'reports': reports
    })
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Report

from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from .models import Report
import io

from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from .models import Report


def download_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    # ✅ CASE 1: FILE EXISTS → download file
    if report.report_file:
        return FileResponse(
            report.report_file.open(),
            as_attachment=True,
            filename=f"report_{report.id}.pdf"
        )

    # ✅ CASE 2: NO FILE → generate full medical text report
    content = f"""
==============================
        MEDICAL REPORT
==============================

Patient Details:
Name: {report.patient.user.username}
Age: {report.age or '-'}
Gender: {report.gender or '-'}
Weight: {report.weight or '-'}

Vitals:
BP: {report.bp or '-'}
Temperature: {report.temperature or '-'}

Medical Details:
Diagnosis: {report.diagnosis or '-'}
Prescription: {report.prescription or '-'}
Notes: {report.notes or '-'}

Doctor: {report.doctor.user.username}
Appointment Token: {report.appointment.token_number}

Generated on: {report.uploaded_at}

==============================
"""

    return HttpResponse(
        content,
        content_type="text/plain",
        headers={
            "Content-Disposition": f'attachment; filename="report_{report.id}.txt"'
        }
    )
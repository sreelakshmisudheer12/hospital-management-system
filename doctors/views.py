from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from .forms import DoctorForm
from .models import Doctor, DoctorSchedule
from datetime import datetime, timedelta
from patients.models import Patient
from appointments.models import Appointment
from feedbacks.models import Feedback
from reports.models import Report


# 📌 DOCTOR LIST
def doctor_list(request):

    doctors = Doctor.objects.filter(approved=True)

    search = request.GET.get('search')

    if search:
        doctors = doctors.filter(
            Q(user__username__icontains=search) |
            Q(department__name__icontains=search)
        )

    return render(request, 'doctor_list.html', {
        'doctors': doctors
    })


# 📌 DOCTOR DETAIL
def doctor_detail(request, pk):

    doctor = get_object_or_404(Doctor, pk=pk, approved=True)

    return render(request, 'doctor_detail.html', {
        'doctor': doctor
    })


# 📌 DOCTOR PROFILE
@login_required
def doctor_profile(request):

    doctor = get_object_or_404(Doctor, user=request.user)

    return render(request, 'doctor_profile.html', {
        'doctor': doctor
    })


# 📌 UPDATE PROFILE
@login_required
def update_doctor_profile(request):

    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)

        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'update_doctor_profile.html', {
        'form': form
    })


# 📌 DOCTOR DASHBOARD (FIXED)
@login_required
def doctor_dashboard(request):

    doctor = Doctor.objects.filter(user=request.user).first()

    if not doctor:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-appointment_date', 'token_number')

    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
    })

def add_schedule(request):

    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == 'POST':

        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        already_exists = DoctorSchedule.objects.filter(
            doctor=doctor,
            day=day,
            start_time=start_time,
            end_time=end_time
        ).exists()

        if already_exists:
            messages.error(request, 'Schedule already exists.')
            return redirect('add_schedule')

        DoctorSchedule.objects.create(
            doctor=doctor,
            day=day,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, 'Schedule added successfully.')
        return redirect('doctor_dashboard')

    schedules = DoctorSchedule.objects.filter(doctor=doctor)

    return render(request, 'add_schedule.html', {
        'schedules': schedules
    })


# 📌 DELETE SCHEDULE
@login_required
def delete_schedule(request, pk):

    doctor = get_object_or_404(Doctor, user=request.user)

    schedule = get_object_or_404(
        DoctorSchedule,
        id=pk,
        doctor=doctor
    )

    schedule.delete()

    messages.success(request, 'Schedule deleted successfully.')
    return redirect('add_schedule')
def get_available_slots(request, doctor_id, date):

    doctor = get_object_or_404(Doctor, id=doctor_id)

    # convert string → date object
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    weekday = date_obj.strftime("%A")

    schedules = DoctorSchedule.objects.filter(
        doctor=doctor,
        day=weekday
    )

    slots = []

    for s in schedules:

        start = datetime.combine(date_obj, s.start_time)
        end = datetime.combine(date_obj, s.end_time)

        while start < end:

            slot_time = start.time()

            # IMPORTANT: compare TIME, not string
            booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=date_obj,
                appointment_time=slot_time,
                status__in=['PENDING', 'APPROVED']
            ).exists()

            if not booked:
                slots.append(slot_time.strftime("%H:%M"))

            start += timedelta(minutes=30)

    return JsonResponse({"slots": slots})
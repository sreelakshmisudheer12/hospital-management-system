from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404

from .models import Department

from doctors.models import Doctor


def department_list(request):

    departments = Department.objects.all()

    return render(request,
                  'department_list.html',
                  {'departments': departments})


def department_detail(request, pk):

    department = get_object_or_404(
        Department,
        id=pk
    )

    doctors = Doctor.objects.filter(
        department=department,
        approved=True
    )

    return render(request,
                  'department_detail.html',
                  {
                      'department': department,
                      'doctors': doctors
                  })
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from .forms import RegisterForm
from .models import CustomUser

from doctors.models import Doctor
from patients.models import Patient


# ---------------- HOME ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- REGISTER ----------------
def register_view(request):

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # SAFE ROLE HANDLING
            role = request.POST.get('role')

            if role:
                role = role.upper()
            else:
                role = 'PATIENT'   # default fallback

            user.role = role
            user.save()

            # CREATE PROFILE BASED ON ROLE
            if role == 'DOCTOR':
                Doctor.objects.create(
                    user=user,
                    approved=False
                )

            elif role == 'PATIENT':
        
                 Patient.objects.get_or_create(user=user
                    
                )

            # LOGIN USER
            login(request, user)

            # ROLE REDIRECT
            if role == 'DOCTOR':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')

    return render(request, 'register.html', {'form': form})


# ---------------- LOGIN ----------------
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        if user.role == 'DOCTOR':
            return '/doctors/dashboard/'
        elif user.role == 'PATIENT':
            return '/patients/dashboard/'
        else:
            return '/'
"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from accounts.views import home


urlpatterns = [

    # HOME PAGE
    path(
        '',
        home,
        name='home'
    ),

    # ADMIN PANEL
    path(
        'admin/',
        admin.site.urls
    ),

    # ACCOUNTS
    path(
        'accounts/',
        include('accounts.urls')
    ),

    # DEPARTMENTS
    path(
        'departments/',
        include('departments.urls')
    ),

    # DOCTORS
    path(
        'doctors/',
        include('doctors.urls')
    ),

    # PATIENTS
    path(
        'patients/',
        include('patients.urls')
    ),

    # APPOINTMENTS
    path(
        'appointments/',
        include('appointments.urls')
    ),

    # REPORTS
    path(
        'reports/',
        include('reports.urls')
    ),

    # FEEDBACKS
    path(
        'feedbacks/',
        include('feedbacks.urls')
    ),
]


# MEDIA FILES

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
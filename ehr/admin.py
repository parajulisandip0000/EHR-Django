from django.contrib import admin

from .models import Doctor, Hospital, Patient, Registration


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "license_number", "phone", "email")
    search_fields = ("name", "license_number", "email")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "specialization", "hospital")
    list_filter = ("hospital", "specialization")
    search_fields = ("first_name", "last_name", "license_number")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "gender", "phone")
    list_filter = ("gender", "blood_group")
    search_fields = ("first_name", "last_name", "phone", "email")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "hospital", "appointment_date", "status")
    list_filter = ("status", "hospital", "appointment_date")
    search_fields = ("patient__first_name", "patient__last_name", "visit_reason")

# Register your models here.

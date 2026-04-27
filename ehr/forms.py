from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Doctor, Hospital, Patient, Registration


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class PatientForm(StyledModelForm):
    class Meta:
        model = Patient
        fields = "__all__"
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "medical_history": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]
        if dob > timezone.localdate():
            raise ValidationError("Date of birth cannot be in the future.")
        return dob


class HospitalForm(StyledModelForm):
    class Meta:
        model = Hospital
        fields = "__all__"
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class DoctorForm(StyledModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"].strip().upper()
        return license_number


class RegistrationForm(StyledModelForm):
    class Meta:
        model = Registration
        fields = [
            "patient",
            "hospital",
            "doctor",
            "appointment_date",
            "visit_reason",
            "notes",
            "status",
        ]
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get("doctor")
        hospital = cleaned_data.get("hospital")
        appointment_date = cleaned_data.get("appointment_date")

        if appointment_date and appointment_date < timezone.localdate() - timezone.timedelta(days=30):
            self.add_error(
                "appointment_date",
                "Appointment date is too far in the past for a new registration.",
            )

        if doctor and hospital and doctor.hospital_id != hospital.id:
            self.add_error(
                "doctor",
                "Selected doctor must belong to the selected hospital.",
            )

        return cleaned_data

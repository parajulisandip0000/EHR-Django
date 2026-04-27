from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PatientForm, RegistrationForm
from .models import Doctor, Hospital, Patient, Registration
from .services import create_registration


class EHRFormTests(TestCase):
    def test_patient_form_rejects_future_dob(self):
        form = PatientForm(
            data={
                "first_name": "Ava",
                "last_name": "Stone",
                "date_of_birth": timezone.localdate() + timezone.timedelta(days=1),
                "gender": "Female",
                "phone": "1234567890",
                "email": "ava@example.com",
                "address": "Kathmandu",
                "blood_group": "A+",
                "emergency_contact": "Mother",
                "medical_history": "",
            }
        )
        self.assertFalse(form.is_valid())


class RegistrationServiceTests(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            name="City Hospital",
            address="Main Road",
            phone="1111111111",
            email="city@example.com",
            license_number="HSP001",
        )
        self.other_hospital = Hospital.objects.create(
            name="Metro Hospital",
            address="Second Road",
            phone="2222222222",
            email="metro@example.com",
            license_number="HSP002",
        )
        self.doctor = Doctor.objects.create(
            first_name="Sam",
            last_name="Taylor",
            specialization="Cardiology",
            license_number="DOC001",
            phone="3333333333",
            email="sam@example.com",
            hospital=self.hospital,
        )
        self.patient = Patient.objects.create(
            first_name="Lina",
            last_name="Khan",
            date_of_birth=timezone.localdate() - timezone.timedelta(days=9000),
            gender="Female",
            phone="4444444444",
            email="lina@example.com",
            address="Kathmandu",
            blood_group="B+",
            emergency_contact="Brother",
            medical_history="",
        )

    def test_create_registration_rejects_wrong_hospital(self):
        with self.assertRaises(ValidationError):
            create_registration(
                patient=self.patient,
                hospital=self.other_hospital,
                doctor=self.doctor,
                appointment_date=timezone.localdate(),
                visit_reason="Follow-up",
                notes="",
                status="Scheduled",
            )

    def test_dashboard_loads(self):
        client = Client()
        response = client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

# Create your tests here.

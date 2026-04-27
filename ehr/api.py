from rest_framework import viewsets

from .models import Doctor, Hospital, Patient, Registration
from .serializers import (
    DoctorSerializer,
    HospitalSerializer,
    PatientSerializer,
    RegistrationSerializer,
)


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related("hospital").all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related("patient", "doctor", "hospital").all()
    serializer_class = RegistrationSerializer

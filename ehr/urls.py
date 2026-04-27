from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import DoctorViewSet, HospitalViewSet, PatientViewSet, RegistrationViewSet
from .views import (
    DashboardView,
    DoctorCreateView,
    DoctorDeleteView,
    DoctorListView,
    DoctorUpdateView,
    HospitalCreateView,
    HospitalDeleteView,
    HospitalListView,
    HospitalUpdateView,
    PatientCreateView,
    PatientDeleteView,
    PatientListView,
    PatientUpdateView,
    RegistrationCreateView,
    RegistrationDeleteView,
    RegistrationListView,
    RegistrationUpdateView,
    SessionHospitalSelectView,
    clear_hospital_session,
)

router = DefaultRouter()
router.register("hospitals", HospitalViewSet)
router.register("doctors", DoctorViewSet)
router.register("patients", PatientViewSet)
router.register("registrations", RegistrationViewSet)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("session/hospital/", SessionHospitalSelectView.as_view(), name="hospital-session"),
    path("session/hospital/clear/", clear_hospital_session, name="hospital-session-clear"),
    path("patients/", PatientListView.as_view(), name="patient-list"),
    path("patients/create/", PatientCreateView.as_view(), name="patient-create"),
    path("patients/<int:pk>/edit/", PatientUpdateView.as_view(), name="patient-update"),
    path("patients/<int:pk>/delete/", PatientDeleteView.as_view(), name="patient-delete"),
    path("hospitals/", HospitalListView.as_view(), name="hospital-list"),
    path("hospitals/create/", HospitalCreateView.as_view(), name="hospital-create"),
    path("hospitals/<int:pk>/edit/", HospitalUpdateView.as_view(), name="hospital-update"),
    path("hospitals/<int:pk>/delete/", HospitalDeleteView.as_view(), name="hospital-delete"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor-create"),
    path("doctors/<int:pk>/edit/", DoctorUpdateView.as_view(), name="doctor-update"),
    path("doctors/<int:pk>/delete/", DoctorDeleteView.as_view(), name="doctor-delete"),
    path("registrations/", RegistrationListView.as_view(), name="registration-list"),
    path("registrations/create/", RegistrationCreateView.as_view(), name="registration-create"),
    path("registrations/<int:pk>/edit/", RegistrationUpdateView.as_view(), name="registration-update"),
    path("registrations/<int:pk>/delete/", RegistrationDeleteView.as_view(), name="registration-delete"),
    path("api/", include(router.urls)),
]

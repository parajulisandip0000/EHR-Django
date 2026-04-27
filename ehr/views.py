from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import DoctorForm, HospitalForm, PatientForm, RegistrationForm
from .models import Doctor, Hospital, Patient, Registration
from .services import create_registration


class DashboardView(TemplateView):
    template_name = "ehr/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_hospital_id = self.request.session.get("selected_hospital_id")
        registrations = Registration.objects.select_related(
            "patient", "doctor", "hospital"
        )
        if selected_hospital_id:
            registrations = registrations.filter(hospital_id=selected_hospital_id)

        context["selected_hospital"] = None
        if selected_hospital_id:
            context["selected_hospital"] = Hospital.objects.filter(
                pk=selected_hospital_id
            ).first()

        context["stats"] = {
            "patients": Patient.objects.count(),
            "doctors": Doctor.objects.count(),
            "hospitals": Hospital.objects.count(),
            "registrations": Registration.objects.count(),
        }
        context["recent_registrations"] = registrations[:5]
        context["hospital_summary"] = Hospital.objects.annotate(
            total_registrations=Count("registrations")
        )
        return context


class SessionHospitalSelectView(TemplateView):
    template_name = "ehr/hospital_session.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hospitals"] = Hospital.objects.all()
        context["selected_hospital_id"] = self.request.session.get("selected_hospital_id")
        return context

    def post(self, request, *args, **kwargs):
        hospital_id = request.POST.get("hospital_id")
        if hospital_id:
            hospital = get_object_or_404(Hospital, pk=hospital_id)
            request.session["selected_hospital_id"] = hospital.pk
            request.session["selected_hospital_name"] = hospital.name
            messages.success(request, f"Session updated for {hospital.name}.")
        return redirect("dashboard")


def clear_hospital_session(request):
    request.session.pop("selected_hospital_id", None)
    request.session.pop("selected_hospital_name", None)
    messages.info(request, "Hospital session data cleared.")
    return redirect("dashboard")


class BaseListView(ListView):
    template_name = "ehr/object_list.html"
    context_object_name = "objects"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["create_url"] = self.create_url
        context["headers"] = self.headers
        context["fields"] = self.fields
        context["entity_name"] = self.entity_name
        return context


class BaseFormViewMixin:
    template_name = "ehr/object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["entity_name"] = self.entity_name
        context["list_url"] = self.list_url
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class BaseDeleteView(DeleteView):
    template_name = "ehr/object_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["entity_name"] = self.entity_name
        context["list_url"] = self.success_url
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class PatientListView(BaseListView):
    model = Patient
    title = "Patients"
    create_url = reverse_lazy("patient-create")
    entity_name = "patient"
    headers = ["Name", "DOB", "Gender", "Phone", "Actions"]
    fields = ["__str__", "date_of_birth", "gender", "phone"]


class PatientCreateView(BaseFormViewMixin, CreateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("patient-list")
    list_url = reverse_lazy("patient-list")
    title = "Create Patient"
    entity_name = "patient"
    success_message = "Patient record created."


class PatientUpdateView(BaseFormViewMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("patient-list")
    list_url = reverse_lazy("patient-list")
    title = "Edit Patient"
    entity_name = "patient"
    success_message = "Patient record updated."


class PatientDeleteView(BaseDeleteView):
    model = Patient
    success_url = reverse_lazy("patient-list")
    title = "Delete Patient"
    entity_name = "patient"
    success_message = "Patient record deleted."


class HospitalListView(BaseListView):
    model = Hospital
    title = "Hospitals"
    create_url = reverse_lazy("hospital-create")
    entity_name = "hospital"
    headers = ["Name", "License", "Phone", "Email", "Actions"]
    fields = ["name", "license_number", "phone", "email"]


class HospitalCreateView(BaseFormViewMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    success_url = reverse_lazy("hospital-list")
    list_url = reverse_lazy("hospital-list")
    title = "Create Hospital"
    entity_name = "hospital"
    success_message = "Hospital record created."


class HospitalUpdateView(BaseFormViewMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    success_url = reverse_lazy("hospital-list")
    list_url = reverse_lazy("hospital-list")
    title = "Edit Hospital"
    entity_name = "hospital"
    success_message = "Hospital record updated."


class HospitalDeleteView(BaseDeleteView):
    model = Hospital
    success_url = reverse_lazy("hospital-list")
    title = "Delete Hospital"
    entity_name = "hospital"
    success_message = "Hospital record deleted."


class DoctorListView(BaseListView):
    model = Doctor
    title = "Doctors"
    create_url = reverse_lazy("doctor-create")
    entity_name = "doctor"
    headers = ["Name", "Specialization", "Hospital", "Phone", "Actions"]
    fields = ["__str__", "specialization", "hospital", "phone"]


class DoctorCreateView(BaseFormViewMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy("doctor-list")
    list_url = reverse_lazy("doctor-list")
    title = "Create Doctor"
    entity_name = "doctor"
    success_message = "Doctor record created."


class DoctorUpdateView(BaseFormViewMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy("doctor-list")
    list_url = reverse_lazy("doctor-list")
    title = "Edit Doctor"
    entity_name = "doctor"
    success_message = "Doctor record updated."


class DoctorDeleteView(BaseDeleteView):
    model = Doctor
    success_url = reverse_lazy("doctor-list")
    title = "Delete Doctor"
    entity_name = "doctor"
    success_message = "Doctor record deleted."


class RegistrationListView(BaseListView):
    model = Registration
    title = "Registrations"
    create_url = reverse_lazy("registration-create")
    entity_name = "registration"
    headers = ["Patient", "Doctor", "Hospital", "Date", "Actions"]
    fields = ["patient", "doctor", "hospital", "appointment_date"]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("patient", "doctor", "hospital")
        selected_hospital_id = self.request.session.get("selected_hospital_id")
        if selected_hospital_id:
            queryset = queryset.filter(hospital_id=selected_hospital_id)
        return queryset


class RegistrationCreateView(BaseFormViewMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    success_url = reverse_lazy("registration-list")
    list_url = reverse_lazy("registration-list")
    title = "Create Registration"
    entity_name = "registration"
    success_message = "Registration record created."

    def form_valid(self, form):
        self.object = create_registration(**form.cleaned_data)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class RegistrationUpdateView(BaseFormViewMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    success_url = reverse_lazy("registration-list")
    list_url = reverse_lazy("registration-list")
    title = "Edit Registration"
    entity_name = "registration"
    success_message = "Registration record updated."


class RegistrationDeleteView(BaseDeleteView):
    model = Registration
    success_url = reverse_lazy("registration-list")
    title = "Delete Registration"
    entity_name = "registration"
    success_message = "Registration record deleted."

# Create your views here.

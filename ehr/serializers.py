from rest_framework import serializers

from .models import Doctor, Hospital, Patient, Registration
from .services import create_registration


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source="hospital.name", read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    hospital_name = serializers.CharField(source="hospital.name", read_only=True)

    class Meta:
        model = Registration
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate(self, attrs):
        doctor = attrs.get("doctor") or getattr(self.instance, "doctor", None)
        hospital = attrs.get("hospital") or getattr(self.instance, "hospital", None)
        if doctor and hospital and doctor.hospital_id != hospital.id:
            raise serializers.ValidationError(
                {"doctor": "Selected doctor must belong to the selected hospital."}
            )
        return attrs

    def create(self, validated_data):
        return create_registration(**validated_data)

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_doctor_name(self, obj):
        return str(obj.doctor)

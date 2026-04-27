from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Registration


@transaction.atomic
def create_registration(**validated_data):
    doctor = validated_data["doctor"]
    hospital = validated_data["hospital"]

    if doctor.hospital_id != hospital.id:
        raise ValidationError("Doctor and hospital association is invalid.")

    registration = Registration(**validated_data)
    registration.full_clean()
    registration.save()
    return registration

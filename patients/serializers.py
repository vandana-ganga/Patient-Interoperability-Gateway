from datetime import date

from rest_framework import serializers

from .models import Patient
from .service import decrypt_value, mask_ssn

class PatientInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        def validate(self, data):
            if data.get("resourceType") != "Patient":
                raise serializers.ValidationError({"resourceType": "Must be Patient."})
            if not data.get("id"):
                raise serializers.ValidationError({"id": "Patient ID is required."})
            
            birth_date = data.get("birthDate")

            if not birth_date:
               raise serializers.ValidationError({ "birthDate": "Birth date is required."})

            try:
                birth_date_obj = date.fromisoformat(birth_date)
            except (ValueError, TypeError):
                raise serializers.ValidationError({"birthDate": "Birth date must be in YYYY-MM-DD format."})

            today = date.today()

            age = today.year - birth_date_obj.year

            if (
                today.month,
                today.day
            ) < (
                birth_date_obj.month,
                birth_date_obj.day
            ):
                age -= 1

            if age < 18:
                raise serializers.ValidationError({"birthDate": "Patient must be at least 18 years old."})
            data["parsed_birth_date"] = birth_date_obj

            return data
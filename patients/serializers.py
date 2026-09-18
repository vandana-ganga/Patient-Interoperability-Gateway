import copy
from datetime import date

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Patient
from .service import encrypt_value, decrypt_value, mask_ssn

SSN_SYSTEM = "http://hl7.org/fhir/sid/us-ssn"

class PatientInputSerializer(serializers.ModelSerializer):
	resourceType = serializers.CharField(write_only=True)
	id = serializers.CharField(source="fhir_patient_id", validators=[UniqueValidator(queryset=Patient.objects.all())],)
	birthDate = serializers.DateField(source="birth_date")
	name = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
	identifier = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
	passportNumber = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Patient
		fields = ["resourceType", "id", "active", "gender", "birthDate", "name", "identifier", "passportNumber"]
	
	def validate_resourceType(self, value):
		if value != "Patient":
			raise serializers.ValidationError("resourceType must be 'Patient'.")
		return value
	
	def validate_birthDate(self, value):
		today = date.today()
		age = today.year - value.year
		if (today.month, today.day) < (value.month, value.day):
			age -= 1

		if age < 18:
			raise serializers.ValidationError("Patient must be at least 18 years old.")

		return value
	
	def _mask_ssn_and_passport_value_in_payload(self, data):
				payload = copy.deepcopy(data)
				for ident in payload.get("identifier", []):
					if ident.get("system") == SSN_SYSTEM:
						ident["value"] = "SSN-VALUE"
				if "passportNumber" in payload:
					payload["passportNumber"] = "PASSPORT-VALUE"
				return payload
	
	def create(self, validated_data):
		validated_data.pop("resourceType")
		names = validated_data.pop("name", [])
		identifiers = validated_data.pop("identifier", [])
		passport_number = validated_data.pop("passportNumber", None)
		first_name = last_name = family_name = None
		if names:
			official_name = next((n for n in names if n.get("use") == "official"), names[0])
			family_name = official_name.get("family")
			given_names = official_name.get("given", [])
			if given_names:
				first_name = given_names[0]
				last_name = " ".join(given_names[1:]) or None

		identifier = {"identifier": identifiers}
		for identifier in identifiers:
			if identifier.get("system") == SSN_SYSTEM:
				ssn = identifier.get("value")
		return Patient.objects.create(
			**validated_data,
			first_name=first_name,
			last_name=last_name,
			family_name=family_name,
			encrypted_ssn=encrypt_value(ssn),
			encrypted_passport_number=encrypt_value(passport_number) if passport_number else None,
			raw_payload=self._mask_ssn_and_passport_value_in_payload(self.initial_data),
		)
		

class PatientResponseSerializer(serializers.ModelSerializer):
	ssn = serializers.SerializerMethodField()
	class Meta:
		model = Patient
		fields = [
			"fhir_patient_id",
			"active",
			"gender",
			"birth_date",
			"ssn",
			"created_at",
		]

	def get_ssn(self, obj):
		if not obj.encrypted_ssn:
			return None
		decrypted_ssn = decrypt_value(obj.encrypted_ssn)
		return mask_ssn(decrypted_ssn)
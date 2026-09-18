from django.db import models
from django.conf import settings

class Patient(models.Model):
	id = models.AutoField(primary_key=True)
	fhir_patient_id = models.CharField(max_length=100, unique=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	family_name = models.CharField(max_length=100, blank=True, null=True)
	birth_date = models.DateField()
	active = models.BooleanField(default=True)
	gender = models.CharField(max_length=10, blank=True, null=True)
	encrypted_ssn = models.TextField(blank=True, null=True)
	encrypted_passport_number = models.TextField(blank=True, null=True)
	raw_payload = models.JSONField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Patient {self.fhir_patient_id}"
		
		
class AccessLog(models.Model):
	patient = models.ForeignKey("Patient", on_delete=models.CASCADE , related_name="access_logs")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
	ip_address = models.GenericIPAddressField()
	accessed_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.patient.fhir_patient_id} - {self.accessed_at}"        
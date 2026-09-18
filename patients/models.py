from django.db import models

# Create your models here.


class Patient(models.Model):
    fhir_patient_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100, blank=True, null=True)
    bith_date = models.DateField()
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10)
    encrypted_ssn = models.BinaryField(blank=True, null=True)
    encrypted_passport_number = models.TextField(blank=True, null=True)
    raw_payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Patient {self.fhir_patient_id}"
        
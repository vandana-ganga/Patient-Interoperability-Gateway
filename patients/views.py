from django.shortcuts import render


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PatientRecord, AccessLog
from .serializers import PatientInputSerializer

from .service import encrypt_value, extract_identifier


class PatientInputView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PatientInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_data = serializer.validated_data
        ssn = extract_identifier(
            patient_data,
            "http://hl7.org/fhir/sid/us-ssn",
        )
        names = patient_data.get("name", [])
        first_name = None
        family_name = None
        given_names = []
        last_name = None
        if names:
            official_name = next(
                (
                    name
                    for name in names
                    if name.get("use") == "official"
                ),
                names[0],
            )
            family_name = official_name.get("family")
            given_names = official_name.get(
                "given",
                []
            )

            if given_names:
                first_name = given_names[0]
                last_name = " ".join(given_names[1:]) if len(given_names) > 1 else None

        patient = PatientRecord.objects.create(
            fhir_patient_id=patient_data["id"],
            first_name=first_name,
            last_name=last_name,
            family_name=family_name,
            birth_date=patient_data["parsed_birth_date"],
            active=patient_data.get("active", True),
            gender=patient_data.get("gender"),
            encrypted_ssn=encrypt_value(ssn),
            raw_payload=request.data,
        )
        return Response(
            {
                "message": "Patient successfully created.",
                "patient_id": patient.fhir_patient_id,
            },
            status=status.HTTP_201_CREATED,
        )

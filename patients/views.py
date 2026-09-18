from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient, AccessLog
import threading

from .serializers import PatientInputSerializer, PatientResponseSerializer


class PatientInputView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = PatientInputSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		patient = serializer.save()
		
		# thread = threading.Thread(
		#     target=send_welcome_email,
		#     args=(patient,)
		# )

		# thread.start()

		return Response(
			{
				"message": "Patient successfully created.",
				"patient_id": patient.fhir_patient_id,
			},
			status=status.HTTP_201_CREATED,
		)
		
class PatientDetailsView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, patient_id):
		try:
			patient = Patient.objects.get(fhir_patient_id=patient_id)
		except Patient.DoesNotExist:
			return Response({"detail": "Patient not found."},status=status.HTTP_404_NOT_FOUND)
		ip_address = request.META.get("REMOTE_ADDR")
		AccessLog.objects.create(
			patient=patient,
			user=request.user,
			ip_address=ip_address
		)
		serializer = PatientResponseSerializer(patient)
		return Response(
			serializer.data,
			status=status.HTTP_200_OK
		)
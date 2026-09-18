import time

# no email we are taking from patient so in background to send email i am printing the mail function 
def send_welcome_email(patient):
	time.sleep(2)

	print(
		f"Welcome email sent for patient: "
		f"{patient.fhir_patient_id}"
	)
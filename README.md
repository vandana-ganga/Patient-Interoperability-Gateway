Patient Interoperability Gateway" (PIGW)
It is a Django service that ingests standard healthcare data (FHIR),sanitizes it for
HIPAA compliance, and exposes it securely to downstream services.

## Features
- FHIR Patient intake: validates resourceType, a unique patient id, and birthDate and min age is 18 and also  background job welcome  email also getting printed 
- Field-level encryption SSN and passport number are encrypted with cryptography and raw json    storage mask with ssn value and passport vale
- Masked output: SSN is returned as ***-**-1234
- when access the patient details  lookup records like user ip address and timestamp is stored 
- JWT authentication: using djangorestframework-simplejwt(access token 30 min, refresh token 1 day)

Tech Stacks
Python, Django, DjangoRest Framework, PostgreSQL

To run this application 
1. git clone https://github.com/vandana-ganga/Patient-Interoperability-Gateway.git
2. cd PIGW
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. create .env file in root directory
        include values 
        DB_NAME="database_name"
        DB_USER="database_user"
        DB_PASSWORD="db_password"
        DB_HOST=localhost
        DB_PORT=5432
        FIELD_ENCRYPTION_KEY="encription_key"

7. To generate a encription key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
8.  python manage.py migrate
9.  python manage.py createsuperuser  create a super user with username email and password values
10. python manage.py runserver


API Endpoints

1. generate token 
  http://127.0.0.1:8000/api/v1/token/ 
   with payload 
        {
            "username":"username",
            "password":"password"
        }
    respose will get access and refresh token    

2. Create a patient 
 http://127.0.0.1:8000/api/v1/patient-intake/
 with payload 
    {
    "resourceType": "Patient", "id":
    "example-125",  "active": true,
    "name": [
    {
    "use": "official", "family":"Chalmers",
    "given":["Peter", "James"]
    }
    ],
    "gender":"male",
    "birthDate": "1980-12-25", "identifier": [
    {
    "system": "http://hl7.org/fhir/sid/us-ssn", "value": "000-12-3456"
    }
    ],
    "telecom": [
    {
    "system": "phone", "value": "(555) 555-5555",
    "use": "home"
    }
    ]
    }
with acesstoken as bearer token

response
{
	"message": "Patient successfully created.",
	"patient_id": "example-125"
}
and in background the welcome email is geting printed 

3. Get patient details 

http://127.0.0.1:8000/api/v1/patients/patient-id/ ---example  http://127.0.0.1:8000/api/v1/patients/example-123/
with acesstoken as bearer token
will get response 

 {
	"fhir_patient_id": "example-123",
	"active": true,
	"gender": "male",
	"birth_date": "1980-12-25",
	"ssn": "***-**-3456",
	"created_at": "2026-09-18T05:23:21.069451Z"
}
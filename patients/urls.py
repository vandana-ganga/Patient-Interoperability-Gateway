from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PatientInputView, PatientDetailsView

urlpatterns = [
	path("patient-intake/", PatientInputView.as_view(), name="patient-input"),
	path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
	path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
	path("patients/<str:patient_id>/", PatientDetailsView.as_view(), name="patient-detail"),
]
from rest_framework import views
from .models import Beds, Ward, Patient , PatientStatus
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST , HTTP_203_NON_AUTHORITATIVE_INFORMATION
# Create your views here.


class CheckBedStatus(views.APIView):
    def post(self, request):
        try:
            bed_number = request.data.get("bed_number")
            beds = Beds.objects.filter(bed_number=bed_number)
            if beds:
                bed = beds.last()
                ward = Ward.objects.filter(bed=bed, patient__patient_status=PatientStatus.ADMIT)
                if ward:
                    room = ward[0]
                    data = []
                    data["status"] = True
                    data["bed_type"] = bed.bed_type
                    data["patient"] = room.patient
                    return Response(data, status=HTTP_200_OK)
                else:
                    result = {"status": True, "data": "Bed is available"}
                    return Response(result, status=HTTP_200_OK)
            else:
                result = {"status": False, "data": "Please Enter Correct Bed number"}
                return Response(result, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            result = {"status": False, "data": "Please check admin"}
            return Response(result, status=HTTP_401_UNAUTHORIZED)


class CheckoutPatient(views.APIView):
    def post(self, request):
        try:
            patient_id = request.data.get("patient_id")
            patient = Patient.objects.filter(id=patient_id)
            if patient:
                patient.update(patient_status=PatientStatus.DISCHARGED)
                wards = Ward.objects.filter(patient=patient[0])
                ward = wards[0]
                bed = ward.bed
                Beds.objects.filter(id=bed.id).update(is_available=True)
                result = {"status": True, "data": "Patient is succesfully checked out"}
                return Response(result, status=HTTP_200_OK)
            else:
                result = {"status": False, "data": "Please enter Correct patient id"}
                return Response(result, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Exception as e:
            print(e)
            result = {"status": False, "data": e}
            return Response(result, status=HTTP_400_BAD_REQUEST)

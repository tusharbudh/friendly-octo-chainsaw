from .models import Beds, Ward


def get_patient_names(bed_type):
    try:
        ward = Ward.objects.filter(bed__type=bed_type)
        pateints = ward.values_list("patient__firstname", flat=True)
        return pateints
    except Exception as e:
        print(e)


def get_status_of_beds(bed_type):
    try:
        beds = Beds.objects.filter(bed_type=bed_type , is_available=True)
        if beds:
            no_of_beds = beds.count()
            return f"Total number of available beds are {no_of_beds}"
        else:
            return "Full"
    except Exception as e:
        print(e)


def free_bed_list():
    try:
        beds = Beds.objects.filter(is_available=True)
        if beds:
            bed_numbers = beds.values_list("bed_number", flat=True)
            return bed_numbers
        else:
            return "full"
    except Exception as e:
        print(e)






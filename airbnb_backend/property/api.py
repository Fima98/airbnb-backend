from django.http import JsonResponse  # type: ignore
from datetime import datetime

from rest_framework.decorators import api_view, authentication_classes, permission_classes  # type: ignore

from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationListSerializer
from .forms import PropertyForm


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properies_list(request):
    properties = Property.objects.all()

    host_id = request.GET.get("host", None)

    if host_id:
        properties = properties.filter(host_id=host_id)

    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()

    serializer = ReservationListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.host = request.user
        property.save()
        return JsonResponse({"success": True, "data": PropertiesListSerializer(property).data})
    print("Error", form.errors, form.non_field_errors)
    return JsonResponse({"success": False, "errors": form.errors.as_json()}, status=400)


@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        guests_str = request.POST.get("guests")

        if not start_date_str or not end_date_str:
            return JsonResponse(
                {"success": False, "message": "Start date and end date are required."},
                status=400
            )

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if start_date >= end_date:
            return JsonResponse(
                {"success": False, "message": "End date must be after start date."},
                status=400
            )

        property_obj = Property.objects.get(pk=pk)

        overlapping_reservations = Reservation.objects.filter(
            property=property_obj,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        if overlapping_reservations.exists():
            return JsonResponse(
                {"success": False, "message": "The property is already reserved for the selected dates."},
                status=400
            )

        nights = (end_date - start_date).days
        base_price = nights * property_obj.price_per_night
        fee = base_price * 0.05
        total_price = base_price + fee

        guests = int(guests_str) if guests_str else 1

        Reservation.objects.create(
            property=property_obj,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user,
        )

        return JsonResponse({
            "success": True,
            "message": "Reservation created successfully.",
            "data": {
                "nights": nights,
                "base_price": base_price,
                "fee": fee,
                "total_price": total_price
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

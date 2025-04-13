from django.http import JsonResponse  # type: ignore
from datetime import datetime

from rest_framework.decorators import api_view, authentication_classes, permission_classes  # type: ignore

from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationListSerializer
from .forms import PropertyForm
from useraccount.models import User
from rest_framework_simplejwt.tokens import AccessToken


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all()
    host_id = request.GET.get("host", None)
    is_favorite = request.GET.get("is_favorites", None)

    country = request.GET.get("country", None)
    category = request.GET.get("category", None)
    check_in = request.GET.get("check_in", None)
    check_out = request.GET.get("check_out", None)
    guests = request.GET.get("guests", None)

    favorites = []

    try:
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        token = AccessToken(token)
        user_id = token.payload.get("user_id")
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None

    if host_id:
        properties = properties.filter(host_id=host_id)

    if is_favorite:
        properties = properties.filter(favorited__in=[user])

    if guests:
        properties = properties.filter(guests__gte=guests)

    if country:
        properties = properties.filter(country_code=country)

    if category:
        properties = properties.filter(category=category)

    if check_in and check_out:
        exect_matches = Reservation.objects.filter(
            start_date=check_in) | Reservation.objects.filter(end_date=check_in)

        overlap_matches = Reservation.objects.filter(
            start_date__lte=check_out, end_date__gte=check_in)
        all_matches = []

        for match in exect_matches | overlap_matches:
            all_matches.append(match.property_id)

        properties = properties.exclude(id__in=all_matches)

    if user:
        for property in properties:
            if user in property.favorited.all():
                favorites.append(property.id)

    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse({'data': serializer.data, 'favorites': favorites})


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
def reserve_property(request, pk):
    try:
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        guests_str = request.POST.get("guests")

        print("INFOooooooo", start_date_str, end_date_str, guests_str)

        print(start_date_str, end_date_str, guests_str)

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


@api_view(['POST'])
def toggle_favorite(request, pk):
    property = Property.objects.get(pk=pk)
    user = request.user

    if user in property.favorited.all():
        property.favorited.remove(user)
        return JsonResponse({"success": True, "is_favorite": False})
    else:
        property.favorited.add(user)
        return JsonResponse({"success": True, "is_favorite": True})

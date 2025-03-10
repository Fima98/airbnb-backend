from django.http import JsonResponse  # type: ignore

from rest_framework.decorators import api_view, authentication_classes, permission_classes  # type: ignore

from .models import Property
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer
from .forms import PropertyForm


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properies_list(request):
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse({"data": serializer.data})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)


@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.host = request.user
        property.save()
        return JsonResponse({"status": "success", "data": PropertiesListSerializer(property).data})
    print("Error", form.errors, form.non_field_errors)
    return JsonResponse({"Errors": form.errors.as_json()}, status=400)

from .serializers import UserDetailSerializer, CustomRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


from property.serializers import ReservationListSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(request=request)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'access': access_token,
                'refresh': refresh_token,
                'message': 'User created successfully!'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def host_detail(request, pk):
    user = User.objects.get(pk=pk)
    serializer = UserDetailSerializer(user, many=False)
    return JsonResponse(serializer.data)


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations_created.all()
    serializer = ReservationListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)

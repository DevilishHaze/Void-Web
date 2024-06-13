from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , permissions , generics
from .serializers import CoordinateSerializer , ConstellationSerializer , ConstellationForAdmin
from .models import Constellation
from .utils import get_visible_constellations


class ConstellationsListAPI(generics.ListCreateAPIView):
    "Только для админов"
    queryset = Constellation.objects.all()
    serializer_class = ConstellationForAdmin
    permission_classes = [permissions.IsAdminUser]


class VisibleConstellationsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CoordinateSerializer)
    def post(self , request):
        print("Request data:" , request.data)
        serializer = CoordinateSerializer(data=request.data)
        if serializer.is_valid():
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']

            visible_constellations = get_visible_constellations(longitude , latitude)
            constellation_serializer = ConstellationSerializer(visible_constellations , many=True ,
                                                               context={'request': request})
            return Response(constellation_serializer.data , status=status.HTTP_200_OK)
        else:
            print("Serializer errors:" , serializer.errors)  # Debugging line to print serializer errors
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

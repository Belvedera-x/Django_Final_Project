from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from homefinder_app.models import Housing
from homefinder_app.serializers.housings import (
    HousingCreateUpdateSerializer,
    HousingListSerializer,
    HousingDetailSerializer
)


class HousingListView(generics.ListAPIView):
    queryset = Housing.objects.all()
    serializer_class = HousingDetailSerializer



class HousingSearchView(generics.ListAPIView):
    serializer_class = HousingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Housing.objects.filter(available=True)
        return queryset



class HousingCreateView(generics.CreateAPIView):
    serializer_class = HousingCreateUpdateSerializer
    queryset = Housing.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class HousingUpdateView(generics.UpdateAPIView):
    serializer_class = HousingCreateUpdateSerializer
    queryset = Housing.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()



class HousingDeleteView(generics.DestroyAPIView):
    serializer_class = HousingDetailSerializer
    queryset = Housing.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        housing = self.get_object()

        if housing.owner != request.user:
            return Response(
                {"detail": "You do not have permission to delete this housing."},
                status=status.HTTP_403_FORBIDDEN
            )

        housing.delete()
        return Response({"detail": "Housing deleted."}, status=status.HTTP_204_NO_CONTENT)



class HousingToggleAvailableView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        housing = get_object_or_404(Housing, pk=pk)

        if housing.owner != request.user:
            return Response(
                {"detail": "You cannot modify this housing."},
                status=status.HTTP_403_FORBIDDEN
            )

        housing.toggle_available()
        return Response({"available": housing.available})
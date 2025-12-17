from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from homefinder_app.filters import HousingFilter
from homefinder_app.permissions.housing import HousingPermission
from homefinder_app.models import Housing

from homefinder_app.serializers.housings import (
    HousingCreateUpdateSerializer,
    HousingListSerializer,
    HousingDetailSerializer
)


class HousingViewSet(viewsets.ModelViewSet):
    queryset = Housing.objects.all()
    permission_classes = [HousingPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HousingFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-price']

    def get_serializer_class(self):
        if self.action == 'list':
            return HousingListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return HousingCreateUpdateSerializer
        return HousingDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HousingToggleAvailableView(APIView):
    permission_classes = [HousingPermission]
    def patch(self, request, pk):
        housing = get_object_or_404(Housing, pk=pk)
        housing.toggle_available()
        return Response({"available": housing.available}, status=status.HTTP_200_OK)
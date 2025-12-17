from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from homefinder_app.models import Booking, User
from homefinder_app.enums import Role
from homefinder_app.serializers.bookings import BookingListSerializer, BookingCreateUpdateSerializer
from homefinder_app.permissions.booking import BookingPermission,BookingActionPermission
from django.utils import timezone

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    permission_classes = [BookingPermission]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookingListSerializer
        return BookingCreateUpdateSerializer

    def get_queryset(self):
        user: User | AnonymousUser = self.request.user
        if user.role == Role.tenant.name:
            return Booking.objects.filter(guest=user)
        elif user.role == Role.owner.name:
            return Booking.objects.filter(housing__owner=user)
        else:
            return Booking.objects.all()

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[BookingActionPermission])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.start_date <= timezone.now().date():
            return Response({"detail": "Нельзя отменить бронирование, которое уже началось"}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({"status": booking.status})

    @action(detail=True, methods=['post'], permission_classes=[BookingActionPermission])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'approved'
        booking.save()
        return Response({"status": booking.status})

    @action(detail=True, methods=['post'], permission_classes=[BookingActionPermission])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()
        return Response({"status": booking.status})
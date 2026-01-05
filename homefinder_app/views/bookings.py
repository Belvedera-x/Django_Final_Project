from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from homefinder_app.models import Booking, User
from homefinder_app.enums import Role, BookingStatus
from homefinder_app.serializers.bookings import BookingListSerializer, BookingCreateUpdateSerializer
from homefinder_app.permissions.booking import BookingPermission,BookingActionPermission
from django.utils import timezone
from django.db import transaction

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
        if booking.status != BookingStatus.pending.name:
            return Response(
                {"detail": "Бронирование уже обработано"},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            booking.status = BookingStatus.confirmed.name
            booking.save(update_fields=['status'])
            Booking.objects.filter(
                housing=booking.housing,
                status=BookingStatus.pending.name,
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            ).exclude(
                id=booking.id
            ).update(status=BookingStatus.rejected.name)
        return Response(
            {"status": booking.status},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[BookingActionPermission])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()
        return Response(
            {"status": booking.status},
            status=status.HTTP_200_OK
        )
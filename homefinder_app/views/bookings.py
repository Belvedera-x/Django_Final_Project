from rest_framework import generics, permissions
from homefinder_app.models.booking import Booking
from homefinder_app.serializers.bookings import BookingCreateUpdateSerializer, BookingListSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
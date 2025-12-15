from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from homefinder_app.enums import BookingStatus
from homefinder_app.models import Housing, Booking, Review
from homefinder_app.serializers.rewiews import ReviewSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        housing_id = self.request.data.get('housing')
        housing = Housing.objects.get(pk=housing_id)
        user = self.request.user

        if user.role != 'tenant':
            raise PermissionDenied("Только арендаторы могут оставлять отзывы.")

        has_booking = Booking.objects.filter(
            housing=housing,
            tenant=user,
            status=BookingStatus.confirmed,
            end_date__lt=timezone.now().date()
        ).exists()

        if not has_booking:
            raise PermissionDenied("Вы можете оставить отзыв только после завершённой брони.")

        serializer.save(author=user, housing=housing)



class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(housing_id=self.kwargs['housing_id'])

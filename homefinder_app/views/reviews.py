from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from homefinder_app.enums import BookingStatus, Role
from homefinder_app.models import Housing, Booking, Review, User
from homefinder_app.serializers.reviews import ReviewSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        housing = get_object_or_404(
            Housing,
            pk=self.kwargs['housing_id']
        )
        user: User | AnonymousUser = self.request.user

        if user.role != 'tenant':
            raise PermissionDenied("Только арендаторы могут оставлять отзывы.")

        has_booking = Booking.objects.filter(
            housing=housing,
            guest=user,
            status=BookingStatus.confirmed,
            end_date__lt=timezone.now().date()
        ).exists()

        if not has_booking:
            raise PermissionDenied("Вы можете оставить отзыв только после завершённой брони.")

        serializer.save(author=user, housing=housing)



class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.filter(housing_id=self.kwargs['housing_id'])

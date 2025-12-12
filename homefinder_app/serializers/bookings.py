from rest_framework import serializers

from homefinder_app.models import Booking



class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'housing',
            'start_date',
            'end_date',
            'status',
            'total_price'
        ]


class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'housing',
            'start_date',
            'end_date',
        ]



from decimal import Decimal

from rest_framework import serializers
from django.utils import timezone
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

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        housing = attrs.get('housing')

        today = timezone.now().date()

        if not start_date or not end_date:
            raise serializers.ValidationError(
                "Заполнить нужно обе даты"
            )

        if start_date >= end_date:
            raise serializers.ValidationError(
                "Начало бронирования должно быть раньше окончания"
            )

        if start_date < today:
            raise serializers.ValidationError(
                "Начало бронирование не должно быть в прошлом"
            )

        days = (end_date - start_date).days

        attrs['total_price'] = Decimal(days) * housing.price

        return attrs



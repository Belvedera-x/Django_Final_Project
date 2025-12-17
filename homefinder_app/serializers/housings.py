from rest_framework import serializers

from homefinder_app.models import Housing



class HousingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = '__all__'


class HousingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = [
            'id',
            'title',
            'city',
            'housing_type',
            'number_of_rooms',
            'price',
            'ratings_count',
        ]


class HousingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = [
            'title',
            'description',
            'city',
            'district',
            'street',
            'price',
            'number_of_rooms',
            'housing_type',

        ]




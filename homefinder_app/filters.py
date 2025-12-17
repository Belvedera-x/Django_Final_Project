import django_filters
from homefinder_app.models import Housing


class HousingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    district = django_filters.CharFilter(field_name='district', lookup_expr='icontains')
    min_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='gte')
    max_rooms = django_filters.NumberFilter(field_name='number_of_rooms', lookup_expr='lte')
    housing_type = django_filters.CharFilter(field_name='housing_type', lookup_expr='iexact')

    class Meta:
        model = Housing
        fields = []
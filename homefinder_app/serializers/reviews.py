from rest_framework import serializers

from homefinder_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'rating',
            'text',
            'created_at'
        ]

        read_only_fields = ['author', 'created_at']
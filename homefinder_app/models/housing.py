from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from homefinder_app.enums import HousingType
from homefinder_app.models.user import User


class Housing(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='housings'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    number_of_rooms = models.PositiveSmallIntegerField()
    housing_type = models.CharField(
        max_length=20,
        choices=HousingType.choices(),
        default=HousingType.apartment.name
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    ratings_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'housings'
        ordering = ['-created_at']
        verbose_name = 'Housing'
        verbose_name_plural = 'Housings'

    def __str__(self):
        return self.title

    def toggle_available(self):
        self.available = not self.available
        self.save()


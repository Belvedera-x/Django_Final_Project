from django.core.exceptions import ValidationError
from django.db import models

from homefinder_app.enums import BookingStatus
from homefinder_app.models.housing import Housing
from homefinder_app.models.user import User


class Booking(models.Model):
    housing = models.ForeignKey(
        Housing,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices(),
        default=BookingStatus.pending.name
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "bookings"
        ordering = ["-created_at"]


    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Дата окончания должна быть позже даты начала")

        if Booking.objects.filter(
                housing=self.housing,
                end_date__gt=self.start_date,
                start_date__lt=self.end_date
        ).exists():
            raise ValidationError("Жильё уже забронировано на эти даты")


    def __str__(self):
        return f"{self.housing.title} - {self.start_date} - {self.end_date}"


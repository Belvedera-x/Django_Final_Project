from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from homefinder_app.models.housing import Housing
from homefinder_app.models.user import User


class Review(models.Model):
    housing = models.ForeignKey(Housing, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")

    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


    class Meta:
        db_table = "reviews"
        ordering = ["-created_at"]
from django.db import models

from homefinder_app.models import Housing


class HousingImage(models.Model):
    housing = models.ForeignKey(
        Housing,
        on_delete=models.CASCADE,
        related_name="images"
    )
    file_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "images"
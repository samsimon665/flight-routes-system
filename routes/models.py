from django.db import models
from django.core.exceptions import ValidationError


class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.code


class Route(models.Model):
    POSITION_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right'),
    )

    from_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='outgoing_routes'
    )

    to_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='incoming_routes'
    )

    position = models.CharField(max_length=5, choices=POSITION_CHOICES)
    duration = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['from_airport', 'position'],
                name='unique_position_per_airport'
            )
        ]
        indexes = [
            models.Index(fields=['from_airport']),
        ]

    def clean(self):
        if self.from_airport == self.to_airport:
            raise ValidationError("Route cannot point to the same airport.")

    def __str__(self):
        return f"{self.from_airport.code} → {self.to_airport.code} ({self.duration})"

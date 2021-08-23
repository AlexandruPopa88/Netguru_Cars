from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Cars(models.Model):
    make = models.CharField(max_length=20, null=False)
    model = models.CharField(max_length=20, null=False)

    def __repr__(self):
        return f"{self.make} {self.model}"

    class Meta:
        unique_together = ('make', 'model')


class CarRatings(models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
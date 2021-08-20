from django.db import models

class Cars(models.Model):
    make = models.CharField(max_length=20, NULL=False)
    model = models.CharField(max_length=20, NULL=False)

    def __repr__(self):
        return f"{self.make} {self.model}"

    class Meta:
        unique_together = ('make', 'model')


class Car_Ratings(models.Model):
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    rating = models.IntegerField()
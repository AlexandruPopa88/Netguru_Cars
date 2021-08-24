from django.test import TestCase
from Cars.models import Cars, CarRatings

class CarsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cars = Cars.objects.create(
            make="Volkswagen",
            model="Golf"
        )
        cls.carratings = CarRatings.objects.create(
            car_id = Cars.objects.get(make="Volkswagen", model="Golf"),
            rating = 5
        )

    def test_Cars_has_info_fields(self):
        self.assertIsInstance(self.cars.make, str)
        self.assertIsInstance(self.cars.model, str)

    def test_CarRatings_has_info_fields(self):
        self.assertIsInstance(self.carratings.car_id, Cars)
        self.assertIsInstance(self.carratings.rating, int)

    def test_repr_is_make_and_model(self):
        text = f"{self.cars.make} {self.cars.model}"
        self.assertEquals(repr(self.cars), text)

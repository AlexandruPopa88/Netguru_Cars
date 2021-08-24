from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from Cars.models import Cars, CarRatings
from Cars.serializers import CarsSerializer
import json

class CarViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cars = [Cars.objects.create(model="Volkswagen", make="Passat"),
                    Cars.objects.create(model="Audi", make="A4"),
                    Cars.objects.create(model="Honda", make="Civic")]
        cls.car = cls.cars[0]

        cls.carratings = [CarRatings.objects.create(car_id=cls.cars[i], rating=1)
                          for i in range(3)]
        cls.carrating = cls.carratings[0]

    def test_car_in_all_cars(self):
        response = self.client.get(reverse("cars:cars_list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.cars), len(json.loads(response.content)))

        all_cars = json.loads(response.content)
        for c in all_cars:
            c.pop('avg_rating')

        for car in self.cars:
            self.assertIn(
                CarsSerializer(instance=car).data,
                all_cars
            )

    def test_can_add_a_new_car(self):
        payload = {"make": "Honda", "model": "S2000"}
        response = self.client.post(reverse("cars:cars_list"), json.dumps(payload), content_type='application/json')
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_can_delete_a_car(self):
        car = Cars.objects.first()
        id = car.id
        self.client.delete(reverse("cars:del_cars", str(id)))
        self.assertNotIn(car, Cars.objects.all())

class PopularViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cars = [Cars.objects.create(model="Volkswagen", make="Passat"),
                    Cars.objects.create(model="Audi", make="A4"),
                    Cars.objects.create(model="Honda", make="Civic")]
        cls.carratings = [CarRatings.objects.create(car_id=cls.cars[i], rating=5)
                          for i in range(3)]
        for _ in range(2):
            CarRatings.objects.create(car_id=cls.cars[2], rating = 1)

    def test_get_popular_cars(self):
        response = self.client.get(reverse("cars:popular"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        popular_cars = json.loads(response.content)
        for i in range(len(popular_cars) -1):
            self.assertGreaterEqual(popular_cars[i]["rates_number"], popular_cars[i+1]["rates_number"])
from django.shortcuts import render
from django.views import View
from Cars.models import Cars, Car_Ratings
import json


class Car_view(View):

    def get(self):
        all_cars = Cars.objects.all()
        for car in all_cars:
            ratings = Car_Ratings.objects.filter(car_id=car)
            car.avg_rating = round(sum(rate.rating for rate in ratings) / len(ratings), 1)
        return all_cars

    def post(self, request):
        data = json.loads(request.body)
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{data['make'].lower()}?format=json"
        check = request.get(url)
        if check.status_code == 200:
            pass
        elif check.status_code == 404:
            raise NameError("Car is not available in database.")
        else:
            raise ConnectionError("Try again later.")

    def delete(self, id):
        Cars.objects.filter(id=id).delete()

class Rate_view(View):

    def post(self, request):
        pass

class Popular_view(View):

    def get(self, request):
        pass


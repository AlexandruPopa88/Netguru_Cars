from django.shortcuts import render
from django.views import View
from Cars.models import Cars, Car_Ratings
from django.http import HttpResponse
import json
import requests


class CarView(View):

    def get(self, request):
        all_cars = Cars.objects.all()
        for car in all_cars:
            ratings = Car_Ratings.objects.filter(car_id=car)
            car.avg_rating = round(sum(rate.rating for rate in ratings) / len(ratings), 1)
        return HttpResponse(json.dumps([{"car": car for car in all_cars}]))

    def post(self, request):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{json_data['make'].lower()}?format=json"
        check = requests.get(url)
        if check.status_code == 200:
            data = check.json()
            if data["Results"] and json_data["model"] in (car["Model_Name"] for car in data["Results"]):
                if not Cars.objects.filter(make=json_data["make"], model=json_data["model"]):
                    Cars.objects.create(make=json_data["make"], model=json_data["model"])
                    return HttpResponse(f'Added car: {json_data["make"]} {json_data["model"]}')
                return HttpResponse("Car already exists")
            return HttpResponse("Car doesn't exist in external API")
        else:
            raise ConnectionError("Try again later.") # nu stiu ce eroare sa pun

    def delete(self, request, del_id):
        if not Cars.objects.filter(id=del_id).exists():
            return HttpResponse("Error")
        Cars.objects.filter(id=del_id).delete()
        return HttpResponse(200)
        # catch return 500

class RateView(View):

    def post(self, request):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        car = Cars.objects.filter(id=json_data["car_id"])
        if car.exists():
            Car_Ratings.objects.create(car_id=car, rating=json_data["rating"])

        # else bad inputs

class PopularView(View):

    def get(self):
        pass
        # data = Cars.objects.filter(Car_Ratings.car_id)
        # Car_Ratings.objects.aggregate()

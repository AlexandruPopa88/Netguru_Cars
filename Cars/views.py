from django.views import View
from Cars.models import Cars, CarRatings
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import json
import requests

def try_catch(original_function):
    def decorated(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        except json.decoder.JSONDecodeError:
            return HttpResponse("JSONDecodeError has occurred, check json keys.", status=400)
        except KeyError:
            return HttpResponse("KeyError has occurred, check json syntax.", status=400)
        except Cars.DoesNotExist:
            return HttpResponse("Car.DoesNotExist has occurred, check id.", status=400)
        except IntegrityError:
            return HttpResponse("IntegrityError has occurred, this car already exists.", status=400)
        except ValidationError:
            return HttpResponse("ValidationError has occurred, the rating must be between 1<=rating<= 5.", status=400)


    return decorated

class CarView(View):

    def get(self, request):
        all_cars = Cars.objects.annotate(avg_rating=Avg("carratings__rating"))
        if all_cars:
            return JsonResponse([{"id": car.id,
                                  "make": car.make,
                                  "model": car.model,
                                  "avg_rating": car.avg_rating} for car in all_cars], safe=False)
        return JsonResponse([], safe=False)

    @try_catch
    def post(self, request):
        json_data = json.loads(request.body)
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{json_data['make'].lower()}?format=json"
        check = requests.get(url)
        if check.status_code == 200:
            data = check.json()
            if data["Results"] and json_data["model"] in (car["Model_Name"] for car in data["Results"]):
                car = Cars(make=json_data["make"], model=json_data["model"])
                car.save()
                return HttpResponse(status=201)
            return HttpResponse("Car doesn't exist in external API", status=400)
        else:
            return HttpResponse("External API threw an error", status=500)

    @try_catch
    def delete(self, request, del_id):
        Cars.objects.get(id=del_id).delete()
        return HttpResponse(status=200)

class RateView(View):

    @try_catch
    def post(self, request):
        json_data = json.loads(request.body)
        car = Cars.objects.get(id=json_data["car_id"])
        rating = CarRatings(car_id=car, rating=json_data["rating"])
        rating.full_clean()
        rating.save()
        return HttpResponse(status=201)

class PopularView(View):

    def get(self, request):
        top_cars = Cars.objects.annotate(rates_number=Count('carratings')).order_by('-rates_number')
        return JsonResponse([{"id": car.id,
                              "make": car.make,
                              "model": car.model,
                              "rates_number": car.rates_number} for car in top_cars], safe=False)



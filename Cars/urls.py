from django.urls import path
from .views import CarView, RateView, PopularView, CarViewSet, CarsRatingsViewSet
from rest_framework.routers import DefaultRouter

app_name = "cars"
router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'cars', CarsRatingsViewSet)
urlpatterns = router.urls

urlpatterns = [
    path('cars/', CarView.as_view(), name="cars_list"),
    path('cars/<int:id>/', CarView.as_view(), name='del_cars'),
    path('rate/', RateView.as_view(), name="rate"),
    path('popular/', PopularView.as_view(), name="popular")
]
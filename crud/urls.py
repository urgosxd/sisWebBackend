from django.urls import path

from crud.views import TourView


urlpatterns = [
         path("tours/",TourView.as_view(),name="tours")
        ]

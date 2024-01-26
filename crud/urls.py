from django.urls import path

from crud.views import FichaTecnicaView, TourView
from rest_framework import routers


router = routers.DefaultRouter()

# router.register(r'tours',TourView, 'tours')

# rout
urlpatterns = [
        path("tours/",TourView.as_view({'get':'list','post':'create'}),name="tours"),
        path("fichaTecnica/",FichaTecnicaView.as_view({'get':'list'}),name="ficha")
        ]

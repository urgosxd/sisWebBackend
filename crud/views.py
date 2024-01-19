from django.shortcuts import render
from rest_framework import viewsets
from crud.models import Tour

from crud.serializer import TourModelSerializer

# Create your views here.

class TourView(viewsets.ModelViewSet):
    serializer_class = TourModelSerializer
    queryset = Tour.objects.all()

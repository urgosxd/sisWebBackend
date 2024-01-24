from dj_rest_auth.views import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets
from crud.models import Tour

from crud.serializer import TourModelSerializer

# Create your views here.

class TourView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = TourModelSerializer
    queryset = Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        
        return [permision() for permision in permission_classes]
    

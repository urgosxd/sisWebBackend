from dj_rest_auth.views import IsAuthenticated
from django.shortcuts import render
from rest_framework import viewsets
from crud.models import FichaTecnica, Tour
import tempfile
import os
from crud.serializer import FichaTecnicaSerializer, TourModelSerializer
from rest_framework.response import Response

from django.contrib.staticfiles.storage import staticfiles_storage
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
    
 # class FichaTecnicaView(viewsets.ModelViewSet):
    # permission_classes = []
def write_file(data, filename,ext):
    fd, path = tempfile.mkstemp(suffix="."+ext,prefix=filename,dir="staticfiles/")
    # Convert binary data to proper format and write it on Hard Disk
    try:
        with os.fdopen(fd, 'w') as tmp:
        # do stuff with temp file
            tmp.write(data)
    finally:
        os.remove(path)

class FichaTecnicaView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = FichaTecnicaSerializer
    queryset = FichaTecnica.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def retrieve(self, request, *args,**kwargs):
    #     instance = self.get_object()
    #     print(dir(instance))
    #     serializer = self.get_serializer(instance)
    #     # write_file(instance.Doc_Content,instance.FileName)
    #     # file_path = staticfiles_storage.path(one.FileName+"."+one.Extension)

    #     return Response(serializer.data)
        




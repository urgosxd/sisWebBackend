import base64
from dj_rest_auth.views import IsAuthenticated
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from crud.models import FichaTecnica, Tour
import tempfile
import os
from crud.serializer import FichaTecnicaSerializer, TourModelSerializer
from rest_framework.response import Response
from django.db import transaction 
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
import json
# Create your views here.

class TourView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = TourModelSerializer
    queryset = Tour.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = []
        else: 
            permission_classes = []
        return [permision() for permision in permission_classes]
    def perform_create(self, serializer,files):
        # print(files[0]["Extension"])
        # print(files[0])
        with transaction.atomic():
            tour = serializer.save()
            for i in files:
                i["Tour"] = tour.id
                format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
                ext = format.split('/')[-1]  # guess file extension
                i["Doc_Content"] = base64.b64decode(filestr).decode('latin-1')
                print((i["Doc_Content"]))
            ga= FichaTecnicaSerializer(data=files,many=True)
            if ga.is_valid():
                ga.save()
            else:
                print(ga.errors)
                print("NOOO")

    def create(self, request, *args, **kwargs):
        # print(request.data)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        self.perform_create(serializer,json.loads(request.data["fichas"]))
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

 # class FichaTecnicaView(viewsets.ModelViewSet):
    # permission_classes = []
def write_file(data, filename,ext):
    print(filename,ext)
    fd, path = tempfile.mkstemp(suffix="."+ext,prefix=filename,dir="staticfiles/")
    # Convert binary data to proper format and write it on Hard Disk
    try:
        with os.fdopen(fd, 'wb') as tmp:
        # do stuff with temp file
            tmp.write(data)
    finally:
        return path

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
    def retrieve(self, request, *args,**kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance)
        path = write_file(instance.Doc_Content,instance.FileName,instance.Extension)
        # file_path = staticfiles_storage.path(one.FileName+"."+one.Extension)
        with open(path,'rb') as pdf:
            response = HttpResponse(pdf.read(),content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{instance.FileName}.pdf"'
            os.remove(path)
            return response



        




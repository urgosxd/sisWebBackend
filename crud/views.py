import base64
from dj_rest_auth.views import APIView, AllowAny, IsAuthenticated
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from requests import delete
from rest_framework import status, viewsets
from crud.models import Boleto, Guiado, Hotel, Notification, Restaurante, Tour, Transporte, Traslado, Tren, UpSelling
import tempfile
import os
from crud.serializer import BoletoModelSerializer, GuiadoModelSerializer, HotelModelSerializer, NotificationSerializer, RestauranteModelSerializer, TourModelSerializer, TransporteModelSerializer, TrasladoModelSerializer, TrenModelSerializer, UpSellingModelSerializer
from rest_framework.response import Response
from django.db import transaction 
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
import json
from django.core.cache import cache
from django.http import JsonResponse
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
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    def perform_create(self, serializer,files):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Tour"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer,None)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    def perform_update(self, serializer,files):
        print(files)
        if files is None:
            serializer.save()
        else:
            with transaction.atomic():
                tour = serializer.save()
                fichasTour= tour.fichasTecnicas.all()
                newFiles = []
                for i in files:
                    if i is not None:
                        format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
                        ext = format.split('/')[-1]  # guess file extension
                        i["Doc_Content"] = base64.b64decode(filestr)
                        ficha = FichaTecnicaSerializer(data=i)
                        if ficha.is_valid():
                            newFiles.append(ficha.save())
                        else:
                            print(ficha.errors)
                    else:
                        newFiles.append(None)
                while len(newFiles) < len(fichasTour):
                    files.append(None)
                newQuerySet = []
                for a ,b in zip(fichasTour,newFiles):
                    if b is not None:
                        newQuerySet.append(b)
                else:
                    newQuerySet.append(a)

                tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer,json.loads(request.data["fichas"]))
        except:
            self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})


class CleanTour(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Tour.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Tour.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})

# class UpdateCurrentTour(APIView):
#     permission_classes= [IsAuthenticated]
#     def put(self,request,pk,format=None):
#         Tour.objects.filter(id=pk).update(current)



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

# class FichaTecnicaView(viewsets.ModelViewSet):
#     # permission_classes = []
#     serializer_class = FichaTecnicaSerializer
#     queryset = FichaTecnica.objects.all()
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'list':
#             permission_classes = []
#         else: 
#             permission_classes = []
#         return [permision() for permision in permission_classes]
#     def retrieve(self, request, *args,**kwargs):
#         instance = self.get_object()
#         # serializer = self.get_serializer(instance)
#         path = write_file(instance.Doc_Content,instance.FileName,instance.Extension)
#         # file_path = staticfiles_storage.path(one.FileName+"."+one.Extension)
#         with open(path,'rb') as pdf:
#             response = HttpResponse(pdf.read(),content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="{instance.FileName}.pdf"'
#             os.remove(path)
#             return response


class NotificationView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = []
    def list(self, request, *args, **kwargs):
        last = Notification.objects.last()
        serialiser = NotificationSerializer(last)
        return Response(serialiser.data)
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
        

# class CurrencyStatus(APIView):
#     permission_classes=[AllowAny]
#     def get(self,request):
#         api_response = cache.get('api_response')
#         if api_response:
#             return JsonResponse(api_response)
#         else:
#             return JsonResponse({'error': 'No hay datos disponibles'}, status=404)

class HotelView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = HotelModelSerializer
    queryset = Hotel.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    def perform_create(self, serializer,files):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Hotel"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer,None)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    def perform_update(self, serializer,files):
        print(files)
        if files is None:
            serializer.save()
        else:
            with transaction.atomic():
                tour = serializer.save()
                fichasTour= tour.fichasTecnicas.all()
                newFiles = []
                for i in files:
                    if i is not None:
                        format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
                        ext = format.split('/')[-1]  # guess file extension
                        i["Doc_Content"] = base64.b64decode(filestr)
                        ficha = FichaTecnicaSerializer(data=i)
                        if ficha.is_valid():
                            newFiles.append(ficha.save())
                        else:
                            print(ficha.errors)
                    else:
                        newFiles.append(None)
                while len(newFiles) < len(fichasTour):
                    files.append(None)
                newQuerySet = []
                for a ,b in zip(fichasTour,newFiles):
                    if b is not None:
                        newQuerySet.append(b)
                else:
                    newQuerySet.append(a)

                tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer,json.loads(request.data["fichas"]))
        except:
            self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanHotel(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Hotel.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Hotel.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})



class RestauranteView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = RestauranteModelSerializer
    queryset = Restaurante.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    def perform_create(self, serializer,files):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer,None)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    def perform_update(self, serializer,files):
        print(files)
        if files is None:
            serializer.save()
        else:
            with transaction.atomic():
                tour = serializer.save()
                fichasTour= tour.fichasTecnicas.all()
                newFiles = []
                for i in files:
                    if i is not None:
                        format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
                        ext = format.split('/')[-1]  # guess file extension
                        i["Doc_Content"] = base64.b64decode(filestr)
                        ficha = FichaTecnicaSerializer(data=i)
                        if ficha.is_valid():
                            newFiles.append(ficha.save())
                        else:
                            print(ficha.errors)
                    else:
                        newFiles.append(None)
                while len(newFiles) < len(fichasTour):
                    files.append(None)
                newQuerySet = []
                for a ,b in zip(fichasTour,newFiles):
                    if b is not None:
                        newQuerySet.append(b)
                else:
                    newQuerySet.append(a)

                tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer,json.loads(request.data["fichas"]))
        except:
            self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanRest(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Restaurante.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Restaurante.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})



class BoletoView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = BoletoModelSerializer
    queryset = Boleto.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanBoleto(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Boleto.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Boleto.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})


class TrasladoView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = TrasladoModelSerializer
    queryset = Traslado.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})


class CleanTraslado(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Traslado.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Traslado.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})

class TrenView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = TrenModelSerializer
    queryset = Tren.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanTren(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Tren.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Tren.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})


class TransporteView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = TransporteModelSerializer
    queryset = Transporte.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanTransporte(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Transporte.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Transporte.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})


class UpSellingView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = UpSellingModelSerializer
    queryset = UpSelling.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})

class CleanUpselling(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            UpSelling.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            UpSelling.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})


class GuiadoView(viewsets.ModelViewSet):
    # permission_classes = []
    serializer_class = GuiadoModelSerializer
    queryset = Guiado.objects.all()
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    # def get_queryset(self):
    #     print(dir(self.request))
    #     return Tour.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'listGAA':
            permission_classes = []
        else: 
            permission_classes = [IsAuthenticated]
        return [permision() for permision in permission_classes]
    # def perform_create(self, serializer,files):
    def perform_create(self, serializer):
        serializer.save()
        # with transaction.atomic():
        #     tour = serializer.save()
        #     for i in files:
        #         i["Restaurante"] = tour.id
        #         format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #         ext = format.split('/')[-1]  # guess file extension
        #         i["Doc_Content"] = base64.b64decode(filestr)
        #     ga= FichaTecnicaSerializer(data=files,many=True)
        #     if ga.is_valid():
        #         ga.save()
        #     else:
        #         print(ga.errors)
        #         print("NOOO")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        # print(request.data["fichas"])
        # self.perform_create(serializer,json.loads(request.data["fichas"]))
        self.perform_create(serializer)
        # print(serializer.errors)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
    # def perform_update(self, serializer,files):
    def perform_update(self, serializer):
        serializer.save()
        # print(files)
        # if files is None:
        #     serializer.save()
        # else:
        #     with transaction.atomic():
        #         tour = serializer.save()
        #         fichasTour= tour.fichasTecnicas.all()
        #         newFiles = []
        #         for i in files:
        #             if i is not None:
        #                 format, filestr = i["Doc_Content"].split(';base64,')  # format ~= data:image/X,
        #                 ext = format.split('/')[-1]  # guess file extension
        #                 i["Doc_Content"] = base64.b64decode(filestr)
        #                 ficha = FichaTecnicaSerializer(data=i)
        #                 if ficha.is_valid():
        #                     newFiles.append(ficha.save())
        #                 else:
        #                     print(ficha.errors)
        #             else:
        #                 newFiles.append(None)
        #         while len(newFiles) < len(fichasTour):
        #             files.append(None)
        #         newQuerySet = []
        #         for a ,b in zip(fichasTour,newFiles):
        #             if b is not None:
        #                 newQuerySet.append(b)
        #         else:
        #             newQuerySet.append(a)

        #         tour.fichasTecnicas.set(newQuerySet)
                               

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={'request':request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # try:
        #     self.perform_update(serializer,json.loads(request.data["fichas"]))
        # except:
        #     self.perform_update(serializer,None)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ga","res"})


class CleanGuiado(APIView):
    permission_classes= [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.data == "None":
            Guiado.objects.filter(id=pk).update(currentUser=None)
            return Response({"ga","res"})
        else:
            Guiado.objects.filter(id=pk).update(currentUser=int(request.data))
            return Response({"ga","res"})


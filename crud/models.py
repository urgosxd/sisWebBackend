from datetime import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,post_delete
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
import json

# Create your models here.

class Document(models.Model):
    Extension = models.CharField(max_length=40, null=True)
    FileName = models.CharField(max_length=200, null=True)
    Doc_Content = models.BinaryField(null=True)
    class Meta:
        abstract=True
class Notification(models.Model):
    message = models.CharField(max_length =300,null=False,blank=False)

class Tour(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    excursion = models.CharField(max_length =100,null=False,blank=False)
    provedor = models.CharField(max_length =100,null=False,blank=False)
    pe = models.DecimalField(max_digits=8, decimal_places=2)
    ppp = models.DecimalField(max_digits=8, decimal_places=2)
    ppe = models.DecimalField(max_digits=8, decimal_places=2)
    pvp = models.DecimalField(max_digits=8, decimal_places=2)
    pve = models.DecimalField(max_digits=8, decimal_places=2)
    recomendacionesImagen = models.CharField(max_length =250,null=False,blank=False)
    fichaTecnica = models.CharField(max_length =250,null=False,blank=False)
    pdfProveedor = models.CharField(max_length =250,null=False,blank=False)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserTour")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()
def NicePrintInstance(instance):
    values = [(k,v) for k,v in instance.__dict__.items() if k != '_state']
    return values

@receiver(post_save,sender=Tour)
def createNotificationTour(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un tour de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("weee")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un tour {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Tour)
def getUpdateNotificationTour(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Tour)
def getDeleteNotificationTour(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un tour de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
    

class FichaTecnica(Document):
    Tour = models.ForeignKey(Tour,on_delete=models.CASCADE,related_name="fichasTecnicas",null=True)




class Hotel(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    clase = models.CharField(max_length =100,null=False,blank=False)
    nombre = models.CharField(max_length =100,null=False,blank=False)
    categoria = models.CharField(max_length =100,null=False,blank=False)
    telefonoReserva = models.CharField(max_length =100,null=False,blank=False)
    telefonoRecepcion = models.CharField(max_length =100,null=False,blank=False)
    precioConfidencial = models.DecimalField(max_digits=8, decimal_places=2)
    simple = models.DecimalField(max_digits=8, decimal_places=2)
    doble = models.DecimalField(max_digits=8, decimal_places=2)
    triple = models.DecimalField(max_digits=8, decimal_places=2)
    horarioDesayunoInicio = models.TimeField()
    horarioDesayunoFinal = models.TimeField()
    checkIn = models.TimeField()
    checkOut = models.TimeField()
    fichaTecnica = models.CharField(max_length =250,null=False,blank=False)
    pdfProveedor = models.CharField(max_length =250,null=False,blank=False)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserHotel")
    lastModify = models.DateTimeField(default=timezone.now())

    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()


class FichaTecnicaHotel(Document):
    Hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name="fichasTecnicas",null=True)

@receiver(post_save,sender=Hotel)
def createNotificationHotel(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un hotel de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un hotel {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Hotel)
def getUpdateNotificationHotel(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Hotel)
def getDeleteNotificationHotel(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un hotel de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
    



class Restaurante(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    nombre = models.CharField(max_length =100,null=False,blank=False)
    categoria = models.CharField(max_length =100,null=False,blank=False)
    especialidad = models.CharField(max_length =100,null=False,blank=False)
    tipoDeServicio = models.CharField(max_length =100,null=False,blank=False)
    horarioDeAtencion = models.CharField(max_length =100,null=False,blank=False)
    direccion = models.CharField(max_length =100,null=False,blank=False)
    telefonoReserva = models.CharField(max_length =100,null=False,blank=False)
    telefonoRecepcion = models.CharField(max_length =100,null=False,blank=False)
    precioCarta = models.DecimalField(max_digits=8, decimal_places=2)
    precioMenu = models.DecimalField(max_digits=8, decimal_places=2)
    fichaTecnica = models.CharField(max_length =250,null=False,blank=False)
    pdfProveedor = models.CharField(max_length =250,null=False,blank=False)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserRest")
    lastModify = models.DateTimeField(default=timezone.now())

    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()

@receiver(post_save,sender=Restaurante)
def createNotificationRest(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un Restaurante de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un Restaurante {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Restaurante)
def getUpdateNotificationRest(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Restaurante)
def getDeleteNotificationRest(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un Restaurante de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 
class FichaTecnicaRestaurante(Document):
    Restaurante = models.ForeignKey(Restaurante,on_delete=models.CASCADE,related_name="fichasTecnicas",null=True)


class Boleto(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    servicio = models.CharField(max_length =100,null=False,blank=False)
    adultop = models.DecimalField(max_digits=8, decimal_places=2)
    adultoe = models.DecimalField(max_digits=8, decimal_places=2)
    niniop = models.DecimalField(max_digits=8, decimal_places=2)
    ninioe = models.DecimalField(max_digits=8, decimal_places=2)
    infantep = models.DecimalField(max_digits=8, decimal_places=2)
    infantee = models.DecimalField(max_digits=8, decimal_places=2)
    estudiantePeruano = models.DecimalField(max_digits=8, decimal_places=2)
    estudianteExtranjero = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserBoleto")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()
    
@receiver(post_save,sender=Boleto)
def createNotificationBoleto(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un Boleto de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un Boleto {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Boleto)
def getUpdateNotificationBoleto(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Boleto)
def getDeleteNotificationBoleto(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un Boleto de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 

class Traslado(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    servicio = models.CharField(max_length =100,null=False,blank=False)
    tipoDeVehiculo = models.CharField(max_length =100,null=False,blank=False)
    precio =  models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserTraslado")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()

@receiver(post_save,sender=Traslado)
def createNotificationTras(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un traslado de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un traslado {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Traslado)
def getUpdateNotificationTras(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Traslado)
def getDeleteNotificationTras(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un traslado de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 


class Tren(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    empresa = models.CharField(max_length =100,null=False,blank=False)
    ruta = models.CharField(max_length =100,null=False,blank=False)
    categoria = models.CharField(max_length =100,null=False,blank=False)
    adulto = models.DecimalField(max_digits=8, decimal_places=2)
    ninio = models.DecimalField(max_digits=8, decimal_places=2)
    infante = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserTren")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()

@receiver(post_save,sender=Tren)
def createNotificationTren(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un tren de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un tren {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Tren)
def getUpdateNotificationTren(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Tren)
def getDeleteNotificationTren(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un tren de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 
 
class Transporte(models.Model):
    ciudad = models.CharField(max_length =100,null=False,blank=False)
    servicio = models.CharField(max_length =100,null=False,blank=False)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserTransporte")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()

@receiver(post_save,sender=Transporte)
def createNotificationTrans(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un transporte de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un transporte {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Transporte)
def getUpdateNotificationTrans(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Transporte)
def getDeleteNotificationTrans(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un transporte de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 
 
class UpSelling(models.Model):
    servicioProducto  = models.CharField(max_length =100,null=False,blank=False)
    detalle = models.CharField(max_length =300,null=False,blank=False)
    pnp = models.DecimalField(max_digits=8, decimal_places=2)
    pne = models.DecimalField(max_digits=8, decimal_places=2)
    pvp = models.DecimalField(max_digits=8, decimal_places=2)
    pve = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserUpselling")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()

@receiver(post_save,sender=UpSelling)
def createNotificationUps(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un UpSelling de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un UpSelling {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=UpSelling)
def getUpdateNotificationUps(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=UpSelling)
def getDeleteNotificationUps(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un UpSelling de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 
 
class Guiado(models.Model):
    servicio  = models.CharField(max_length =100,null=False,blank=False)    
    idioma = models.CharField(max_length =100,null=False,blank=False)    
    detalle = models.CharField(max_length =300,null=False,blank=False)
    precioPullp = models.DecimalField(max_digits=8, decimal_places=2)
    precioPulle = models.DecimalField(max_digits=8, decimal_places=2)
    precioPrivadop = models.DecimalField(max_digits=8, decimal_places=2)
    precioPrivadoe = models.DecimalField(max_digits=8, decimal_places=2)
    lastAccessUser = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    currentUser = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,related_name="currentUserGuiado")
    lastModify = models.DateTimeField(default=timezone.now())
    def __eq__(self, other):
        if other is None:
            return True
        # print("EQ")
        values = [(k,v) for k,v in self.__dict__.items() if k != '_state']
        other_values = [(k,v) for k,v in other.__dict__.items() if k != '_state']
        # for i in values:
        #     for e in other_values:
        #         if i[1] != e[1]:
        #             return False
        return values == other_values
    def __hash__(self):
        return super().__hash__()


@receiver(post_save,sender=Guiado)
def createNotificationGuia(sender,instance,created,**kwargs):
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    if not created:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.__dict__} a {instance.__dict__}  a las {currentTime}")
            Notification.objects.create(message=f"{instance.lastAccessUser} actualizo un Guiado de {NicePrintInstance(instance.__prev)} a {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
        else:
            print("WAA")
    else:
        if instance.__prev != instance:
            # print(f"{instance.lastAccessUser} actualizo un tour de {instance.__prev.ciudad} a {instance.ciudad}  a las {datetime.now()}")
            print("")
        else:
            Notification.objects.create(message=f"{instance.lastAccessUser} creo un Guiado {NicePrintInstance(instance)}  a las {currentTime}")
            sender.objects.filter(id = instance.id).update(lastModify=current_datetime,currentUser=instance.lastAccessUser)


@receiver(pre_save,sender=Guiado)
def getUpdateNotificationGuia(sender,instance,**kwargs):
    prev = None
    if instance.id:
       prev = sender.objects.get(id = instance.id)
       # print("prev",prev)
    instance.__prev = prev
    print(instance.__prev)


@receiver(post_delete,sender=Guiado)
def getDeleteNotificationGuia(sender,instance,**kwargs):
    # print(f"{instance.lastAccessUser} borro un tour de {instance.__dict__}")
    current_datetime = datetime.now()
    currentTime = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
    Notification.objects.create(message=f"{instance.lastAccessUser} borro un Guiado de {NicePrintInstance(instance)} a las {currentTime}")
    sender.objects.filter(id = instance.id).update(lastModify=current_datetime)
 



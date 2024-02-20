from django.urls import include, path

from crud.views import BoletoView, FichaTecnicaView, GuiadoView, HotelView, RestauranteView, TourView,NotificationView, TransporteView, TrasladoView, TrenView, UpSellingView
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'ficha',FichaTecnicaView, 'ficha')
router2 = routers.DefaultRouter()
router2.register(r'tour',TourView, 'tour')

router3 = routers.DefaultRouter()
router3.register(r'notification',NotificationView,'notification')

router4 = routers.DefaultRouter()
router4.register(r'hotel',HotelView,'hotel')


router5 = routers.DefaultRouter()
router5.register(r'restaurante',RestauranteView,'restaurante')


router6 = routers.DefaultRouter()
router6.register(r'boleto',BoletoView,'boleto')


router7 = routers.DefaultRouter()
router7.register(r'traslado',TrasladoView,'traslado')

router8 = routers.DefaultRouter()
router8.register(r'tren',TrenView,'tren')


router9 = routers.DefaultRouter()
router9.register(r'transporte',TransporteView,'transporte')


router10 = routers.DefaultRouter()
router10.register(r'upselling',UpSellingView,'upselling')


router11 = routers.DefaultRouter()
router11.register(r'guiado',GuiadoView,'guiado')

urlpatterns = [
        path("tours/",include(router2.urls)),
        path("fichaTecnica/",include(router.urls)),
        path("notification/",include(router3.urls)),
        path("hoteles/",include(router4.urls)),
        path("restaurantes/",include(router5.urls)),
        path("boletos/",include(router6.urls)),
        path("traslados/",include(router7.urls)),
        path("trenes/",include(router8.urls)),
        path("transportes/",include(router9.urls)),
        path("upsellings/",include(router10.urls)),
        path("guiados/",include(router11.urls)),
        
        # path("currency/",CurrencyStatus.as_view())
        ]

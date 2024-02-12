from django.urls import include, path

from crud.views import FichaTecnicaView, TourView,NotificationView
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'ficha',FichaTecnicaView, 'ficha')
router2 = routers.DefaultRouter()
router2.register(r'tour',TourView, 'tour')

router3 = routers.DefaultRouter()
router3.register(r'notification',NotificationView,'notification')


urlpatterns = [
        path("tours/",include(router2.urls)),
        path("fichaTecnica/",include(router.urls)),
        path("notification/",include(router3.urls))
        ]

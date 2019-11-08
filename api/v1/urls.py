

from rest_framework import routers

from api.v1.views import DatasetViewSet

router = routers.DefaultRouter()

router.register(r'events', DatasetViewSet)
from .api.viewset import EntregaView
from django.urls import path

urlpatterns = [

    path("api/v1/entrega/",
         EntregaView.as_view({"post": "create"}),
         name="create entrega"),

    path("api/v1/upgrade_entrega_date/<str:uf>/<int:sla>",
         EntregaView.as_view({"put": "upgrade"}),
         name="upgrade entrega"),

    path("api/v1/entrega/<str:uf>",
         EntregaView.as_view({"get": "retrieve"}),
         name="retrieve entrega"),

    path("api/v1/entrega",
         EntregaView.as_view({"get": "list"}),
         name="list o entrega"
         )

]
# 51829d16-dbd5-41d0-acb9-8d080adb64d8
urlpatterns = urlpatterns

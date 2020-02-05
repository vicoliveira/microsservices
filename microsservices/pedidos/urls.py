from django.urls import path
from .api.viewset import PedidoView

urlpatterns = [

    path("api/v1/pedido/",
         PedidoView.as_view({"post": "create"}),
         name="create new pedido"),

    path("api/v1/pedido/<uuid:pk>/",
         PedidoView.as_view({"get": "retrieve"}),
         name="retrieve pedido"),

    path("api/v1/pedido/<str:uf>/",
         PedidoView.as_view({"get": "list"}),
         name="list pedidos"),

    path("api/v1/pedido",
         PedidoView.as_view({"get": "list_all"}),
         name="list all pedidos"),

    path("api/v1/pedido_status/<uuid:pk>/<str:sts>/",
         PedidoView.as_view({"put": "confirm_delivery_view"}),
         name="confirm delivery"),

]
# 51829d16-dbd5-41d0-acb9-8d080adb64d8
urlpatterns = urlpatterns

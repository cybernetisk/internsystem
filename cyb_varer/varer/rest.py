from rest_framework import viewsets, filters
from cyb_varer.varer.serializers import *
from cyb_varer.varer.models import *

class KontoViewSet(viewsets.ModelViewSet):
    queryset = Konto.objects.all()
    serializer_class = KontoSerializer

class RåvareViewSet(viewsets.ModelViewSet):
    queryset = Råvare.objects.all()
    serializer_class = RåvareSerializer

class LeverandørViewSet(viewsets.ModelViewSet):
    queryset = Leverandør.objects.all()
    serializer_class = LeverandørSerializer

class RåvareprisViewSet(viewsets.ModelViewSet):
    queryset = Råvarepris.objects.all()
    serializer_class = RåvareprisSerializer

class SalgsvareViewSet(viewsets.ModelViewSet):
    queryset = Salgsvare.objects.all()
    serializer_class = SalgsvareSerializer

class SalgsvareRåvareViewSet(viewsets.ModelViewSet):
    queryset = SalgsvareRåvare.objects.all()
    serializer_class = SalgsvareRåvareSerializer

class SalgsvarePrisViewSet(viewsets.ModelViewSet):
    queryset = SalgsvarePris.objects.all()
    serializer_class = SalgsvarePrisSerializer

class SalgskalkyleViewSet(viewsets.ModelViewSet):
    queryset = Salgskalkyle.objects.all()
    serializer_class = SalgskalkyleSerializer

class SalgskalkyleVareViewSet(viewsets.ModelViewSet):
    queryset = SalgskalkyleVare.objects.all()
    serializer_class = SalgskalkyleVareSerializer

class VaretellingViewSet(viewsets.ModelViewSet):
    queryset = Varetelling.objects.all()
    serializer_class = VaretellingSerializer

class VaretellingVareViewSet(viewsets.ModelViewSet):
    queryset = VaretellingVare.objects.all()
    serializer_class = VaretellingVareSerializer

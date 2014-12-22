from rest_framework import viewsets
from rest_framework import filters

from varer.serializers import *
from varer.models import *


class KontoViewSet(viewsets.ModelViewSet):
    queryset = Konto.objects.all()
    serializer_class = KontoSerializer

class RåvareViewSet(viewsets.ModelViewSet):
    queryset = Råvare.objects.all()
    filter_fields = ('navn', 'kategori', 'status', 'innkjopskonto__innkjopskonto')
    search_fields = ['kategori', 'navn', 'innkjopskonto__innkjopskonto']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RåvareWriteSerializer
        return RåvareReadSerializer


class LeverandørViewSet(viewsets.ModelViewSet):
    queryset = Leverandør.objects.all()
    serializer_class = LeverandørSerializer

class RåvareprisViewSet(viewsets.ModelViewSet):
    queryset = Råvarepris.objects.all()
    serializer_class = RåvareprisSerializer

class SalgsvareViewSet(viewsets.ModelViewSet):
    queryset = Salgsvare.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SalgsvareWriteSerializer
        return SalgsvareReadSerializer

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

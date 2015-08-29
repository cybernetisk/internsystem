from rest_framework import viewsets
from rest_framework import filters

from varer.serializers import *
from varer.models import *


class KontoViewSet(viewsets.ModelViewSet):
    queryset = Konto.objects.all()
    serializer_class = KontoSerializer

class RåvareViewSet(viewsets.ModelViewSet):
    queryset = Råvare.objects\
        .prefetch_related('priser__leverandor')\
        .prefetch_related('lenket_salgsvare__priser')\
        .prefetch_related('lenket_salgsvare__raavarer')\
        .all()

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
    queryset = Salgsvare.objects\
        .select_related('salgskonto')\
        .prefetch_related('priser')\
        .prefetch_related('salgsvareråvare_set__raavare__innkjopskonto')\
        .prefetch_related('salgsvareråvare_set__raavare__priser__leverandor')\
        .all()

    filter_fields = ('navn', 'kategori', 'status', 'kassenr')

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
    def get_queryset(self):
        if self.action == 'list':
            return Salgskalkyle.objects.all()
        else:
            return Salgskalkyle.objects\
                .prefetch_related('salgskalkylevare_set__salgsvare__salgskonto')\
                .prefetch_related('salgskalkylevare_set__salgsvare__raavarer')\
                .all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SalgskalkyleWriteSerializer
        elif self.action == 'list':
            return SalgskalkyleReadListSerializer
        else:
            return SalgskalkyleReadItemSerializer


class SalgskalkyleVareViewSet(viewsets.ModelViewSet):
    queryset = SalgskalkyleVare.objects.all()
    serializer_class = SalgskalkyleVareSerializer

class VaretellingViewSet(viewsets.ModelViewSet):
    queryset = Varetelling.objects.prefetch_related('varetellingvare_set__raavare__innkjopskonto').all()
    queryset = Varetelling.objects.prefetch_related('varetellingvare_set__raavare__priser__leverandor').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return VaretellingWriteSerializer
        return VaretellingReadSerializer

class VaretellingVareViewSet(viewsets.ModelViewSet):
    queryset = VaretellingVare.objects.all()
    serializer_class = VaretellingVareSerializer

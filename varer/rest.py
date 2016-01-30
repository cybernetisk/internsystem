from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response


from varer.serializers import *
from varer.models import *


class BaseVarerViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class KontoViewSet(BaseVarerViewSet):
    queryset = Konto.objects.all()
    serializer_class = KontoSerializer


class RåvareViewSet(BaseVarerViewSet):
    queryset = Råvare.objects \
        .prefetch_related('priser__leverandor') \
        .prefetch_related('lenket_salgsvare__priser') \
        .prefetch_related('lenket_salgsvare__raavarer') \
        .all()

    filter_fields = ('navn', 'kategori', 'status', 'innkjopskonto__innkjopskonto')
    search_fields = ['kategori', 'navn', 'innkjopskonto__innkjopskonto']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RåvareWriteSerializer
        return RåvareReadSerializer


class LeverandørViewSet(BaseVarerViewSet):
    queryset = Leverandør.objects.all()
    serializer_class = LeverandørSerializer


class RåvareprisViewSet(BaseVarerViewSet):
    queryset = Råvarepris.objects.all()
    serializer_class = RåvareprisSerializer


class SalgsvareViewSet(BaseVarerViewSet):
    queryset = Salgsvare.objects \
        .select_related('salgskonto') \
        .prefetch_related('priser') \
        .prefetch_related('salgsvareråvare_set__raavare__innkjopskonto') \
        .prefetch_related('salgsvareråvare_set__raavare__priser__leverandor') \
        .all()

    filter_fields = ('navn', 'kategori', 'status', 'kassenr')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SalgsvareWriteSerializer
        return SalgsvareReadSerializer


class SalgsvareRåvareViewSet(BaseVarerViewSet):
    queryset = SalgsvareRåvare.objects.all()
    serializer_class = SalgsvareRåvareSerializer


class SalgsvarePrisViewSet(BaseVarerViewSet):
    queryset = SalgsvarePris.objects.all()
    serializer_class = SalgsvarePrisSerializer


class SalgskalkyleViewSet(BaseVarerViewSet):
    def get_queryset(self):
        if self.action == 'list':
            return Salgskalkyle.objects.all()
        else:
            return Salgskalkyle.objects \
                .prefetch_related('salgskalkylevare_set__salgsvare__salgskonto') \
                .prefetch_related('salgskalkylevare_set__salgsvare__raavarer') \
                .all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SalgskalkyleWriteSerializer
        elif self.action == 'list':
            return SalgskalkyleReadListSerializer
        else:
            return SalgskalkyleReadItemSerializer


class SalgskalkyleVareViewSet(BaseVarerViewSet):
    queryset = SalgskalkyleVare.objects.all()
    serializer_class = SalgskalkyleVareSerializer


class VaretellingViewSet(BaseVarerViewSet):
    queryset = Varetelling.objects.prefetch_related('varetellingvare_set__raavare__innkjopskonto').all()
    queryset = Varetelling.objects.prefetch_related('varetellingvare_set__raavare__priser__leverandor').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return VaretellingWriteSerializer
        elif self.action in ['list']:
            return VaretellingListSerializer
        return VaretellingReadSerializer


class VaretellingVareViewSet(BaseVarerViewSet):
    queryset = VaretellingVare.objects.all()
    serializer_class = VaretellingVareSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from varer.models import (
    Konto,
    Råvare,
    Leverandør,
    Råvarepris,
    Salgsvare,
    SalgsvareRåvare,
    SalgsvarePris,
    Salgskalkyle,
    SalgskalkyleVare,
    Varetelling,
    VaretellingVare,
)
from varer.permissions import VaretellingVarePermissions, VaretellingPermissions
from varer.serializers import (
    KontoSerializer,
    RåvareWriteSerializer,
    RåvareReadSerializer,
    LeverandørSerializer,
    RåvareprisSerializer,
    SalgsvareWriteSerializer,
    SalgsvareReadSerializer,
    SalgsvareRåvareSerializer,
    SalgsvarePrisSerializer,
    SalgskalkyleWriteSerializer,
    VaretellingVareExpandedSerializer,
    VaretellingVareSerializer,
    VaretellingReadSerializer,
    VaretellingReadExpandedSerializer,
    VaretellingListSerializer,
    VaretellingWriteSerializer,
    SalgskalkyleVareSerializer,
    SalgskalkyleReadItemSerializer,
    SalgskalkyleReadListSerializer,
)


class BaseVarerViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class KontoViewSet(BaseVarerViewSet):
    queryset = Konto.objects.all()
    serializer_class = KontoSerializer


class RåvareViewSet(BaseVarerViewSet):
    queryset = (
        Råvare.objects.prefetch_related("priser__leverandor")
        .prefetch_related("lenket_salgsvare__priser")
        .prefetch_related("lenket_salgsvare__raavarer")
        .all()
    )

    filter_fields = (
        "navn",
        "type",
        "kategori",
        "status",
        "innkjopskonto__innkjopskonto",
    )
    search_fields = [
        "kategori",
        "navn",
        "type",
        "mengde",
        "innkjopskonto__gruppe",
        "innkjopskonto__navn",
    ]
    ordering_fields = (
        "navn",
        "kategori",
        "status",
        "innkjopskonto__gruppe",
        "innkjopskonto__innkjopskonto",
        "innkjopskonto__navn",
    )

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return RåvareWriteSerializer
        return RåvareReadSerializer


class LeverandørViewSet(BaseVarerViewSet):
    queryset = Leverandør.objects.all()
    serializer_class = LeverandørSerializer


class RåvareprisViewSet(BaseVarerViewSet):
    queryset = Råvarepris.objects.prefetch_related("leverandor").order_by("-dato").all()
    serializer_class = RåvareprisSerializer

    filter_fields = ("bestillingskode", "leverandor", "aktiv", "raavare")


class SalgsvareViewSet(BaseVarerViewSet):
    queryset = (
        Salgsvare.objects.select_related("salgskonto")
        .prefetch_related("priser")
        .prefetch_related("salgsvareråvare_set__raavare__innkjopskonto")
        .prefetch_related("salgsvareråvare_set__raavare__priser__leverandor")
        .all()
    )

    filter_fields = ("navn", "kategori", "status", "kassenr")
    ordering_fields = ("navn", "kategori", "status", "kassenr")

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return SalgsvareWriteSerializer
        return SalgsvareReadSerializer


class SalgsvareRåvareViewSet(BaseVarerViewSet):
    queryset = SalgsvareRåvare.objects.all()
    serializer_class = SalgsvareRåvareSerializer


class SalgsvarePrisViewSet(BaseVarerViewSet):
    queryset = SalgsvarePris.objects.all()
    serializer_class = SalgsvarePrisSerializer


class SalgskalkyleViewSet(BaseVarerViewSet):
    ordering_fields = ("navn", "dato")

    def get_queryset(self):
        if self.action == "list":
            return Salgskalkyle.objects.all()
        else:
            return (
                Salgskalkyle.objects.prefetch_related(
                    "salgskalkylevare_set__salgsvare__salgskonto"
                )
                .prefetch_related("salgskalkylevare_set__salgsvare__raavarer")
                .all()
            )

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return SalgskalkyleWriteSerializer
        elif self.action == "list":
            return SalgskalkyleReadListSerializer
        else:
            return SalgskalkyleReadItemSerializer


class SalgskalkyleVareViewSet(BaseVarerViewSet):
    queryset = SalgskalkyleVare.objects.all()
    serializer_class = SalgskalkyleVareSerializer


class VaretellingViewSet(BaseVarerViewSet):
    queryset = Varetelling.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        VaretellingPermissions,
    )
    ordering_fields = (
        "id",
        "sted",
        "antall",
        "antallpant",
        "raavare",
        "time_price",
        "added_by",
        "time_added",
    )

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return VaretellingWriteSerializer
        elif self.action in ["list"]:
            return VaretellingListSerializer
        elif "expand" in self.request.query_params:
            return VaretellingReadExpandedSerializer
        return VaretellingReadSerializer

    def get_queryset(self):
        if "expand" not in self.request.query_params:
            return self.queryset

        return (
            self.queryset.prefetch_related(
                "varetellingvare_set__raavare__innkjopskonto"
            )
            .prefetch_related("varetellingvare_set__raavare__priser__leverandor")
            .prefetch_related("varetellingvare_set__added_by")
        )


class VaretellingVareViewSet(BaseVarerViewSet):
    queryset = VaretellingVare.objects.all()
    ordering_fields = (
        "id",
        "time_price",
        "time_added",
    )
    filter_fields = ("varetelling",)
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        VaretellingVarePermissions,
    )

    def get_serializer_class(self):
        if "expand" in self.request.query_params:
            return VaretellingVareExpandedSerializer
        return VaretellingVareSerializer

    def get_queryset(self):
        if "expand" not in self.request.query_params:
            return self.queryset

        return (
            self.queryset.prefetch_related("raavare__innkjopskonto")
            .prefetch_related("raavare__priser__leverandor")
            .prefetch_related("added_by")
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["varetelling"].is_locked:
            raise PermissionDenied(
                detail=_("The inventory count is locked for editing")
            )

        serializer.save(added_by=request.user)
        return Response(
            VaretellingVareExpandedSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
        )

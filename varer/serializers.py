from core.serializers import UserSimpleSerializer
from rest_framework import serializers

from varer.models import *


class KontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konto
        depth = 2


class KontoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konto
        fields = ('id', 'navn', 'gruppe', 'kommentar')


class RåvareWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Råvare
        fields = (
            'kategori', 'navn', 'mengde', 'enhet', 'mengde_svinn', 'antall', 'innkjopskonto', 'status',
            'lenket_salgsvare')
        depth = 0


class RåvareReadSerializer(serializers.ModelSerializer):
    class Priser(serializers.ModelSerializer):
        class Meta:
            model = Råvarepris
            fields = ('id', 'bestillingskode', 'pris', 'pant', 'dato', 'leverandor', 'type', 'aktiv')
            depth = 1

    class Salgsvare(serializers.ModelSerializer):
        class SalgsvarePriser(serializers.ModelSerializer):
            class Meta:
                model = SalgsvarePris
                depth = 0

        priser = SalgsvarePriser(many=True)

        class Meta:
            model = Salgsvare
            depth = 0

    priser = Priser(many=True, read_only=True)
    lenket_salgsvare = Salgsvare()

    class Meta:
        model = Råvare
        fields = (
            'id', 'kategori', 'navn', 'mengde', 'enhet', 'mengde_svinn', 'antall', 'innkjopskonto', 'status', 'priser',
            'lenket_salgsvare')
        depth = 1


class LeverandørSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leverandør


class RåvareprisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Råvarepris


class SalgsvareWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salgsvare
        fields = ('kategori', 'navn', 'salgskonto', 'status', 'raavarer')


class SalgsvareReadSerializer(serializers.ModelSerializer):
    class SalgsvareRåvarer(serializers.ModelSerializer):
        class RåvareItem(serializers.ModelSerializer):
            class Priser(serializers.ModelSerializer):
                class Meta:
                    model = Råvarepris
                    fields = ('id', 'bestillingskode', 'pris', 'pant', 'dato', 'leverandor', 'type', 'aktiv')
                    depth = 1

            priser = Priser(many=True)

            class Meta:
                model = Råvare
                fields = (
                    'id', 'kategori', 'navn', 'mengde', 'enhet', 'mengde_svinn', 'antall', 'innkjopskonto', 'status',
                    'priser')
                depth = 1

        raavare = RåvareItem()

        class Meta:
            model = SalgsvareRåvare
            fields = ('id', 'mengde', 'raavare')
            depth = 1

    class SalgPriser(serializers.ModelSerializer):
        class Meta:
            model = SalgsvarePris
            fields = ('id', 'status', 'dato', 'mva', 'pris_intern', 'pris_ekstern')
            depth = 0

    raavarer = SalgsvareRåvarer(many=True, source='salgsvareråvare_set')
    priser = SalgPriser(many=True)

    class Meta:
        model = Salgsvare
        depth = 1


class SalgsvareRåvareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgsvareRåvare


class SalgsvarePrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgsvarePris


class SalgskalkyleReadItemSerializer(serializers.ModelSerializer):
    class SalgskalkyleVare(serializers.ModelSerializer):
        class Meta:
            model = SalgskalkyleVare
            depth = 2
            fields = ('id', 'interngrad', 'antall', 'salgsvare')

    varer = SalgskalkyleVare(many=True, source='salgskalkylevare_set')

    class Meta:
        model = Salgskalkyle
        depth = 1
        fields = ('id', 'navn', 'kommentar', 'dato', 'varer')


class SalgskalkyleReadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salgskalkyle
        fields = ('id', 'navn', 'kommentar', 'dato')


class SalgskalkyleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salgskalkyle
        fields = ('id', 'navn', 'kommentar', 'dato')


class SalgskalkyleVareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgskalkyleVare


class VaretellingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varetelling
        fields = ('id', 'tittel', 'kommentar', 'tid', 'ansvarlig')


class VaretellingReadSerializer(serializers.ModelSerializer):
    class VaretellingVare(serializers.ModelSerializer):
        class Meta:
            model = VaretellingVare
            depth = 0
            fields = ('id', 'sted', 'antall', 'antallpant', 'kommentar', 'raavare', 'time_price', 'added_by',
                      'time_added')

    varer = VaretellingVare(many=True, source='varetellingvare_set')

    class Meta:
        model = Varetelling
        depth = 1
        fields = ('id', 'tittel', 'kommentar', 'tid', 'ansvarlig', 'varer')


class VaretellingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varetelling
        depth = 1
        fields = ('id', 'tittel', 'kommentar', 'tid', 'ansvarlig')


class VaretellingVareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaretellingVare


class VaretellingVareExpandedSerializer(serializers.ModelSerializer):
    class VaretellingRåvareSerializer(serializers.ModelSerializer):
        class Priser(serializers.ModelSerializer):
            class Meta:
                model = Råvarepris
                fields = ('pris', 'pant', 'dato', 'aktiv')
                depth = 1

        innkjopskonto = KontoSimpleSerializer()
        priser = Priser(many=True, read_only=True)

        class Meta:
            model = Råvare
            fields = ('id', 'kategori', 'navn', 'mengde', 'enhet', 'mengde_svinn', 'antall', 'innkjopskonto',
                      'status', 'priser',)

    added_by = UserSimpleSerializer()
    raavare = VaretellingRåvareSerializer()

    class Meta:
        model = VaretellingVare
        fields = ('id', 'sted', 'antall', 'antallpant', 'kommentar', 'raavare', 'time_price', 'added_by',
                  'time_added')


class VaretellingReadExpandedSerializer(serializers.ModelSerializer):
    varer = VaretellingVareExpandedSerializer(many=True, source='varetellingvare_set')

    class Meta:
        model = Varetelling
        depth = 1
        fields = ('id', 'tittel', 'kommentar', 'tid', 'ansvarlig', 'varer')

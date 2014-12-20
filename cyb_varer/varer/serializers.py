from cyb_varer.varer.models import *
from rest_framework import serializers

class KontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konto
        depth = 2

class RåvareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Råvare
        depth = 1

class LeverandørSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leverandør

class RåvareprisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Råvarepris

class SalgsvareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salgsvare

class SalgsvareRåvareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgsvareRåvare

class SalgsvarePrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgsvarePris

class SalgskalkyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salgskalkyle

class SalgskalkyleVareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalgskalkyleVare

class VaretellingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Varetelling

class VaretellingVareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaretellingVare

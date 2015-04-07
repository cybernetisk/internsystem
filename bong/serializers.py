from rest_framework import serializers
from bong.models import *

class BongLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BongLog

class BongWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = BongWallet
from rest_framework import viewsets
from bong.serializers import BongLogSerializer, BongWalletSerializer
from bong.models import BongLog, BongWallet

# Create your views here.
class BongLogSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bonglogs to be viewed or edited.
    """
    queryset = BongLog.objects.all()
    serializer_class = BongLogSerializer

class BongWalletSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bonglogs to be viewed or edited.
    """
    queryset = BongWallet.objects.all()
    serializer_class = BongWalletSerializer
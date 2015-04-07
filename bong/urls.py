from django.conf.urls import url, include
from rest_framework import routers
from bong.views import BongLogSet, BongWalletSet

bongRouter = routers.DefaultRouter()
bongRouter.register(r'bonglog', BongLogSet)
bongRouter.register(r'bongwallet', BongWalletSet)


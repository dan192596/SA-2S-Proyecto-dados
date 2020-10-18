from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests
import random

# Create your views here.
class DadoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, quantity):
        dados_array=[]
        for i in range(quantity):
            dados_array.append(random.randrange(1,7))
        response = {
            "dados":dados_array
        }
        return Response(response, status=status.HTTP_200_OK)
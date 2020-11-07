from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

import requests
import random
import os
import jwt

# Create your views here.
class DadoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, quantity):
        if os.environ['REVISAR_JWT'] =='True':            
            authorizationHeader = request.META.get('HTTP_AUTHORIZATION')
            token = authorizationHeader.split()            
            f = open(os.environ['PUBLIC_JWT'], "r")
            public_key = f.read()
            jwt.unregister_algorithm('RS256')
            jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
            jwt_options = {
                'verify_signature': False,
                'verify_exp': False,
                'verify_nbf': False,
                'verify_iat': False,
                'verify_aud': False
            }
            data = jwt.decode(token[1], public_key, options=jwt_options, algorithm='RS256')
            valid = False                
            for scope in data['scopes']:
                if scope == "dados.tirar":
                    valid = True
            print("Scopes de token "+str(data['scopes']))
            print("El scope buscado es dados.tirar, el token es "+str(valid))
            if not valid:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        dados_array=[]
        for i in range(quantity):
            dados_array.append(random.randrange(1,7))
        response = {
            "dados":dados_array
        }
        print("Dados retornados: "+str(dados_array))
        return Response(response, status=status.HTTP_200_OK)
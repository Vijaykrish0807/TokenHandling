from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import CustomUser
from django.shortcuts import get_object_or_404
@api_view(['POST'])
def login(request):
    user= get_object_or_404(CustomUser,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found"},status=status.HTTP_404_NOT_FOUND)
    token, created=Token.objects.get_or_create(user=user)
    serializer= UserSerializer(instance=user)
    return Response({"token":token.key, "user": serializer.data})
    

@api_view(['POST'])
def signup(request):
    data= request.data.copy()
    if 'role' not in data:
        data['role']='user' #Default value
    serializer= UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user=CustomUser.objects.get(username= data['username'])
        user.set_password(data['password'])
        user.save()
        token= Token.objects.create(user=user)
        return Response({"token":token.key, "user": serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.role))
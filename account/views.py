from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from account.renderers import HouseOwnerRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#Generate Token Manually
def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    renderer_classes=[HouseOwnerRenderer]
    def post(self, request, format=None):
        serializer= UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token= get_tokens_for_user(user)
            return Response({'token': token, 'msg':'Registration Succsesful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[HouseOwnerRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            print(email, password)
            user=authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                token= get_tokens_for_user(user)
                return Response({'token': token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
    
class TestView(APIView):
    renderer_classes=[HouseOwnerRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response({'msg':'Test Success', 'data':serializer.data}, status=status.HTTP_200_OK)
        
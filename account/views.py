import random
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer, UserEmailOTPSerializer
from account.renderers import HouseOwnerRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import HouseOwner

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
    
class UserEmailOTPView(APIView):
    def post(self, request, format=None):
        serializer = UserEmailOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
            send_mail(
                'Your OTP',
                f'Your OTP is: {otp}',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )
            request.session['otp'] = otp  # Store OTP in session for verification
            return Response({'msg': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserEmailOTPLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserEmailOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            source_email = serializer.data.get('email')
            otp = serializer.data.get('otp')
            stored_otp = request.session.get('otp')
            if stored_otp == otp:
                del request.session['otp']  # Remove OTP from session after successful verification
                user = HouseOwner.objects.get(email=source_email)
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['OTP is not valid']}}, status=status.HTTP_404_NOT_FOUND)



class ProfileView(APIView):
    renderer_classes=[HouseOwnerRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response({'msg':'Test Success', 'data':serializer.data}, status=status.HTTP_200_OK)
        
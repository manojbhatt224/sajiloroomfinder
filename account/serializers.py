from rest_framework import serializers
from account.models import HouseOwner
from django.core.validators import validate_email

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model=HouseOwner
        fields=['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}   
        }
    # Validating Password and Confirm Password while Registration
    def validate(self,attrs):
        email=attrs.get('email')
        if validate_email(email):
            raise serializers.ValidationError('Please provide appropriate email!')
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password didnt match!')
        return attrs
    def create(self, validated_data):
        return HouseOwner.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model= HouseOwner
        fields=['email', 'password']
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=HouseOwner
        fields=['id', 'email', 'first_name', 'last_name']

class UserEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


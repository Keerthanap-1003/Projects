from rest_framework import serializers
from .models import UserRegistration
from users_management.validator import validate_first_name,validate_last_name,validate_email,validate_phone_number,validate_address,validate_pin_code,validate_dob,validate_user_type,validate_username,validate_password

#Serializer class for registering details
class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ('id', 'firstName', 'lastName', 'email', 'phoneNumber', 'username', 'address', 'pinCode', 'dob', 'userType', 'approvalStatus', 'password')
    firstName = serializers.CharField(validators=[validate_first_name])
    lastName = serializers.CharField(validators=[validate_last_name])
    email=serializers.EmailField(validators=[validate_email])
    phoneNumber=serializers.CharField(validators=[validate_phone_number])
    username=serializers.CharField(validators=[validate_username])
    address=serializers.CharField(validators=[validate_address])
    pinCode=serializers.CharField(validators=[validate_pin_code])
    dob=serializers.DateField(validators=[validate_dob])
    userType=serializers.CharField(validators=[validate_user_type])
    password=serializers.CharField(validators=[validate_password])

#Serializer class to update user details
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ('firstName', 'lastName', 'email', 'phoneNumber', 'address', 'pinCode')
    firstName = serializers.CharField(validators=[validate_first_name],required=False)
    lastName = serializers.CharField(validators=[validate_last_name],required=False)
    email=serializers.EmailField(validators=[validate_email],required=False)
    phoneNumber=serializers.CharField(validators=[validate_phone_number],required=False)
    address=serializers.CharField(validators=[validate_address],required=False)
    pinCode=serializers.CharField(validators=[validate_pin_code],required=False)
 
#Serializer class to login users
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ProfileSerializer(serializers.Serializer):
    firstName=serializers.CharField()
    lastName=serializers.CharField()
    email=serializers.EmailField()
    address=serializers.CharField()
    phoneNumber=serializers.CharField()
    pinCode=serializers.CharField()
    dob=serializers.DateField()
   
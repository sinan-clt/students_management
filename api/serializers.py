from rest_framework import serializers
from api.models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class UserSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        
        fields = kwargs.pop('fields', None)

        
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    class Meta:
        model=User
        fields = ('id','username','email','phone_number','name','password','is_gmail_authenticated')


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
           refresh = RefreshToken.for_user(user)
  

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': str(refresh.access_token),
            'access': str(refresh)
        }


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class StaffManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('staff_no','department',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name','description','start_date','end_date',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('staff_no','department',)
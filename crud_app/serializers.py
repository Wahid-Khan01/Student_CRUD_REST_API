from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate_personal_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Personal phone number must be a 10-digit number.")
        return value

class LoginSerializer(serializers.Serializer):
    personal_phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        personal_phone_number = data.get('personal_phone_number')
        password = data.get('password')

        if personal_phone_number and password:
            student = authenticate(username=personal_phone_number, password=password)
            if student is None:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'personal_phone_number' and 'password'")

        data['student'] = student
        return data
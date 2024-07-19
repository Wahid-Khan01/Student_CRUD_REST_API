from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .authentication import CustomAuthentication
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        student = serializer.save()
        student.set_password(student.personal_phone_number)
        student.save()
    def get_queryset(self):
        queryset = Student.objects.all()
        personal_phone_number = self.request.query_params.get('personal_phone_number', None)
        if personal_phone_number is not None:
            queryset = queryset.filter(personal_phone_number=personal_phone_number)
        return queryset

class StudentRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            personal_phone_number = serializer.validated_data['personal_phone_number']
            if Student.objects.filter(personal_phone_number=personal_phone_number).exists():
                return Response({"detail": "Student with this personal phone number already exists."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            student = serializer.save()
            student.set_password(student.personal_phone_number)
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['student']
            return Response({
                'personal_phone_number': user.personal_phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

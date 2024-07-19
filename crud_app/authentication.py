# crud_app/authentication.py
from django.contrib.auth.backends import BaseBackend
from .models import Student

class CustomAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = Student.objects.get(personal_phone_number=username)
            if student.check_password(password):
                return student
        except Student.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None

    def authenticate_header(self, request):
        return 'Basic realm="api"'

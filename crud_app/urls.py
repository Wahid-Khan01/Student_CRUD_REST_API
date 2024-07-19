from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentRegistrationView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', StudentRegistrationView.as_view(), name='student-registration'),
    path('login/', LoginView.as_view(), name='student-login')
]

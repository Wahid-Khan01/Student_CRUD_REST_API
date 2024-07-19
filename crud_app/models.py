from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class StudentManager(BaseUserManager):
    def create_user(self, personal_phone_number, password=None, **extra_fields):
        if not personal_phone_number:
            raise ValueError('The Personal Phone Number field must be set')
        user = self.model(personal_phone_number=personal_phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, personal_phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(personal_phone_number, password, **extra_fields)

class Student(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    in_which_class = models.CharField(max_length=50)
    school_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_phone_number = models.CharField(max_length=15)
    mother_phone_number = models.CharField(max_length=15)
    personal_phone_number = models.CharField(max_length=15, unique=True)
    

    USERNAME_FIELD = 'personal_phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    objects = StudentManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)

class UserRegistration(AbstractUser):

    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username=models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=10,null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='')
    pinCode = models.CharField(max_length=6,default='0')
    dob = models.DateField(null=True)
    userType = models.CharField(max_length=30)
    approvalStatus = models.CharField(max_length=50,default='pending')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName','userType','approvalStatus']

    def __str__(self):
        return self.firstName
    def save(self, *args, **kwargs):
        if not self.password.startswith('bcrypt_sha256$'):
            self.password = make_password(self.password)
        super(UserRegistration, self).save(*args, **kwargs)
    
    
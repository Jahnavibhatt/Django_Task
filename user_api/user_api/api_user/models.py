from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager class for user profile"""

    def create_user(self, email, name, password, user_type, phone):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address.')
        if not password:
            raise ValueError('Users must have a password.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, user_type=user_type, phone=phone)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create super user"""
        user = self.create_user(email, name, password, "", "")

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=255, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'type']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


class Service(models.Model):
    """ Database model for Services """
    service_name = models.CharField(max_length=255)
    service_desc = models.CharField(max_length=255)
    service_provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='services')
    no_of_requests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """ Database model to add comments. """
    request = models.ForeignKey('RequestService',on_delete=models.CASCADE, related_name= 'comments',null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='comments')
    content = models.CharField(max_length=255)


class RequestService(models.Model):
    """ Database model for requested services by customer. """
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requestmade')
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=False , related_name='request')
    request_desc = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    request_updated_at = models.DateTimeField(auto_now=True)


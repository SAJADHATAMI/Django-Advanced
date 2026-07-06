from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserManager(BaseUserManager):
    """
    custom user manager for our custom user
    email instead of user name for identify our user
    """
    def create_user(self, email,password, **extra_fields):
        """
        regular user creation method
        """
        if not email:
            raise ValueError(_("Email is required."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, email,password, **extra_fields):
        """
        admin user creation method
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("super user must have is_staff True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("super user must have is_superuser True"))
        return self.create_user(email,password,**extra_fields)
        

        
    


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model for our app"""
    objects = UserManager()
    email = models.EmailField(max_length=250, unique=True)
    # is staff has access to admin panel
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True,null=True)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email 



@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
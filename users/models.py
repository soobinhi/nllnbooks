from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, user_id, name, password):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email = self.normalize_email(email),
            user_id = user_id,
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, name, password=None):
        user = self.create_user(
            email,
            password = password,
            user_id = user_id,
            name = name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    user_id = models.CharField(primary_key=True, max_length=10, unique=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.user_id
    @property    
    def is_superuser(self):        
        return self.is_admin  

    @property    
    def is_staff(self):       
        return self.is_admin    
        
    def has_perm(self, perm, obj=None):       
        return self.is_admin    
        
    def has_module_perms(self, app_label):       
        return self.is_admin    
        
    @is_staff.setter    
    def is_staff(self, value):      
        self._is_staff = value
    
class Userlog(models.Model):
    user_id = models.CharField(max_length=10)
    login_date = models.DateTimeField()

    
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обов\'язковий')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)
        return self.create_user(email, password, **extra_fields)

ROLE_CHOICES = ((0, 'visitor'), (1, 'admin'))

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    middle_name = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=100, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Методи для адмінки
    def has_perm(self, perm, obj=None): return True
    def has_module_perms(self, app_label): return True
    @property
    def is_staff(self): return self.role == 1

    def __str__(self):
        return f"{self.email} ({self.get_role_name()})"

    @staticmethod
    def get_by_id(user_id):
        try: return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist: return None

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    @staticmethod
    def create(email, password, first_name='', middle_name='', last_name=''):
        user = CustomUser(email=email, first_name=first_name, 
                          middle_name=middle_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def to_dict(self):
        return {
            'id': self.id, 'email': self.email, 'first_name': self.first_name,
            'last_name': self.last_name, 'role': self.role, 'is_active': self.is_active
        }

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role, 'visitor')
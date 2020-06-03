from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """ """

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user """

        if not email:
            raise ValueError('Users must have a valid email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password):
        """Create and save a new staff(admin) user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_teacher(self, email, password):
        """Create and save a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_student(self, email, password):
        """Create and save a new student user"""
        user = self.create_user(email, password)
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_parent(self, email, password):
        """Create and save a new parent user"""
        user = self.create_user(email, password)
        user.is_parent = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def name(self):
        return self.email

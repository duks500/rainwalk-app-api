from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _

from model_utils import Choices


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    # Customer importand information
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Other infromation
    phone_number = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        default='0000000000'
        )
    zipcode = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        default='00000'
        )

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Pet(models.Model):
    """Pet object"""

    SPECIES_LIST = Choices(
        (0, 'cat', _('Cat')),
        (1, 'dog', _('Dog')),
        (2, 'horse', _('Horse')),
    )

    BREED_LIST = Choices(
        (0, 'bulldog', _('Bulldog')),
        (1, 'pug', _('Pug')),
        (2, 'boxer', _('Bocer')),
    )

    pet_name = models.CharField(max_length=255)
    pet_species = models.PositiveSmallIntegerField(
        choices=SPECIES_LIST,
        default=SPECIES_LIST.cat
        )
    pet_breed = models.PositiveSmallIntegerField(
        choices=BREED_LIST,
        default=BREED_LIST.bulldog
        )
    pet_age = models.PositiveIntegerField()
    user = models.ForeignKey(
        # The model for the foreignKey
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.pet_name

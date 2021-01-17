from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _
# US STATES
import core.constants.states as states

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
    address_1 = models.CharField(
        max_length=255,
        default='',
        null=False,
        blank=False
    )
    address_2 = models.CharField(
        max_length=255,
        default='',
        null=False,
        blank=False
    )
    city = models.CharField(
        max_length=255,
        default='',
        null=False,
        blank=False
    )
    zipcode = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        default='00000'
    )
    state = models.CharField(
        blank=True,
        max_length=2,
        choices=states.STATE_CHOICES
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


class Policy(models.Model):
    """Policy to be assign to the pet"""

    PREMIUM_LIST = Choices(
        (0, 'silver', _('Silver')),
        (1, 'gold', _('Gold')),
        (2, 'platinum', _('Platinum')),
    )
    policy_number = models.CharField(
        max_length=255,
        default='12345',
        null=False,
        blank=False
    )
    policy_premium = models.PositiveSmallIntegerField(
        choices=PREMIUM_LIST,
        default=PREMIUM_LIST.silver
    )
    policy_deductible = models.PositiveIntegerField(default=0)
    policy_coinsurance = models.PositiveIntegerField(default=0)
    policy_limit = models.PositiveIntegerField(default=0)
    policy_discount = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.policy_number

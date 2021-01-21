from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _
# LISTS
import core.constants.states as states
import core.constants.breed_list as breed_list
import core.constants.age_list as age_list
import core.constants.policy_limit_factor_list as policy_limit_factor_list

import uuid

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


class Policy(models.Model):
    """Policy to be assign to the pet"""

    PREMIUM_LIST = Choices(
        (0, 'silver', _('Silver')),
        (1, 'gold', _('Gold')),
        (2, 'platinum', _('Platinum')),
    )
    policy_number = models.CharField(
        unique=True,
        max_length=255,
        default='12345',
        null=False,
        blank=False
    )
    policy_premium = models.PositiveSmallIntegerField(
        choices=PREMIUM_LIST,
        default=PREMIUM_LIST.silver
    )
    policy_quate_number = models.OneToOneField(
        'Quate',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.policy_number


class Quate(models.Model):
    """Quate to be assign to user later on"""

    GENDER_LIST = Choices(
        ('Cat', ['Male', 'Female']),
        ('Dog', ['Male', 'Female'])
    )
    BREEDING_ENDORSEMENT_LIST = Choices(
        ('No'),
        ('Male'),
        ('Female')
    )
    quate_id = models.CharField(
        max_length=255,
        primary_key=True,
        unique=True, default=uuid.uuid4,
        blank=False,
        null=False,
    )
    pet_name = models.CharField(
        max_length=255,
        default='MAX'
    )
    base_rate = models.DecimalField(
        default=54.11,
        max_digits=4,
        decimal_places=2
    )
    geographical_factor = models.DecimalField(
        default=0,
        max_digits=4,
        decimal_places=2
    )
    gender_factor = models.CharField(
        blank=True,
        max_length=6,
        choices=GENDER_LIST,
    )
    breed_factor = models.CharField(
        blank=True,
        max_length=255,
        choices=breed_list.BREED_LIST
    )
    age_factor = models.CharField(
        blank=True,
        max_length=255,
        choices=age_list.AGE_LIST
    )
    policy_limit_factor = models.CharField(
        blank=True,
        max_length=255,
        choices=policy_limit_factor_list.POLICY_LIMIT_FACTOR_LIST
    )
    deductibale_factor = models.PositiveIntegerField(
        default=500
    )
    coinsurance_factor = models.PositiveIntegerField(
        default=50,
    )
    exam_fee_factor = models.BooleanField(
        default=False
    )
    holistic_alternative_treatment_factor = models.BooleanField(
        default=False
    )
    boarding_advertising_holoday_cancellation_rate = models.BooleanField(
        default=False
    )
    breeding_endorsement = models.CharField(
        blank=True,
        max_length=255,
        choices=BREEDING_ENDORSEMENT_LIST
    )
    discount_factor = models.CharField(
        blank=True,
        max_length=255,
    )
    digital_partner_factor = models.BooleanField(
        default=False
    )
    affinity_group_factor = models.BooleanField(
        default=False
    )
    smart_collar_factor = models.BooleanField(
        default=False
    )
    employee_benefit_factor = models.DecimalField(
        default=0,
        max_digits=4,
        decimal_places=2
    )

    def __str__(self):
        return self.quate_id

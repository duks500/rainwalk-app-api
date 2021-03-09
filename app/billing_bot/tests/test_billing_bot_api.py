from django.contrib.auth import get_user_model
from django.test import TestCase

import datetime


class PaymentUnitTest(TestCase):
    """Test for payment unit model"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@rainwalk.io',
            'password12345'
        )

    def test_has_paid(self):
        """Test if the user just paid"""
        self.assertFalse(
            self.user.has_paid_for_current_month(),
            "Initial user should have empty paid_until attr",
        )

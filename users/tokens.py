from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


"""
Django has internal APIs for creating One Time Link with user details. 
PasswordResetTokenGenerator API is used for generating token. 
We will extend PasswordResetTokenGenerator with our class to generate a unique token. 
This will make use of your SECRET_KEY of your project.
"""


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()

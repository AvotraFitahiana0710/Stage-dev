from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from Administrateur.models import UserAccount

class UserAccountBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserAccount.objects.get(username=username)
            if user.is_active and check_password(password, user.password):
                return user
        except UserAccount.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return None

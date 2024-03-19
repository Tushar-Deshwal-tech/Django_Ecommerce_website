# your_app/custom_auth.py

from django.contrib.auth.backends import ModelBackend
from .models import UserData

class UserDataBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserData.objects.get(email=email)
            if user.password == password:
                return user
        except UserData.DoesNotExist:
            return None

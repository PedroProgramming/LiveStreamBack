from django.db.models import Q
from django.http import HttpRequest
from django.contrib.auth.backends import ModelBackend, UserModel



class CustomBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.filter(Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return

        if user.exists():
            my_user = user.first()
            if my_user.check_password(password):
                print('1', my_user.id)
                print('2', my_user.pk)
                return my_user
            return
        else:
            return

import jwt

from django.conf import settings

from .models import User
import json


def jwt_authenticate(request):
    PREFIX = "Bearer"
    request.user = None

    try:
        prefix, token = request.headers.get('Authorization').split(" ", 2)
    except:
        return None

    if (not prefix) or (not token):
        return None

    if prefix.lower() != PREFIX.lower():
        return None
    print(token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except:
        return None
        # msg = 'Invalid authentication. Could not decode token.'
        # raise exceptions.AuthenticationFailed(msg)
    print("payload:", payload)

    try:
        user = User.objects.get(pk=payload['userId'])
    except User.DoesNotExist:
        return None
        # msg = 'No user matching this token was found.'
        # raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        return None
        # msg = 'This user has been deactivated.'
        # raise exceptions.AuthenticationFailed(msg)

    return (user, token)

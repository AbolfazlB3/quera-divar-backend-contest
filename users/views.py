from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from grpc import StatusCode
from django.contrib import auth
from .models import User, UserManager

from .auth import jwt_authenticate
import json
import traceback

# Create your views here.


@csrf_exempt
def login(request):
    try:
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        user = User.objects.get(email=body['email'])
        return HttpResponse(user.token)
    except:
        return JsonResponse({'error': {'enMessage': 'Bad Request!'}}, status=400)


@csrf_exempt
def signup(request):
    try:
        body = json.loads(request.body)
        email = body['email']
        name = body['name']
        password = body['password']
        try:
            user = User.objects.get(email=body['email'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email, name=name, password=password)
            user.save()

            print(user)
            return JsonResponse({
                "token": user.token,
                "message": "successfull"
            })

        raise Exception()
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return JsonResponse({'error': {'enMessage': 'Bad Request!'}}, status=400)
    pass


def bank(request):
    user_token = jwt_authenticate(request)
    if user_token == None:
        return HttpResponse("Not Logged In")
    user, token = user_token
    return HttpResponse("user: " + str(user) + "<br/>token:" + token)

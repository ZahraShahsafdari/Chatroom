import uuid

from django.contrib.auth import authenticate, login 
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'GET':
        return render(
            request,
            'login.html',
            context = {
            }
        )
    elif request.method == 'POST':
        user =  authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
         )
        if user is not None:
            login(request, user)
            response = redirect(
                '/chat/'
            )
            return response
        else:
            return HttpResponse("User not found", status = 404)

def index(request):
    return HttpResponse("Hello World")


def validate_user_add_request(data):
    if len(data['firstname']) < 2:
        return False, 'Firstname must be more than 3 characters', 'firstname'
    return True, ''


def user_list(request):
    if request.method == 'POST':
        validate = validate_user_add_request(request.POST)
        if validate[0]:
            u = User(
                firstname=request.POST['firstname'],
                lastname=request.POST['lastname'],
                username=request.POST['username'],
                password='123qwe',
                avatar='123qwe.png'
            )
            try:
                u.save()
            except:
                return HttpResponse(
                    "Duplicate",
                    status = 400
                )
            return HttpResponse("OK")
        else:
            return HttpResponse("Error", status = 400)

    elif request.method == 'GET':
        users = User.objects.all()
        return render(
            request,
            'list.html',
            context={
                'users': users,
                'title': "Users List",
                'test_dict': {
                    "name": "value"
                }
            }
        )

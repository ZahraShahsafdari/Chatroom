from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from message.models import Messages
from message.models import Conversations, ConversationMembers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def add_message(request):
    print(request.COOKIES, type(request.COOKIES))
    if 'token' in request.COOKIES:
        token = request.COOKIES['token']

        try:
            u = User.objects.get(token=token)
            c = Conversations.objects.get( id = request.POST['c_id'])
            m = Messages(
                text = request.POST['text'],
                sender = u,
                conversation = c
            )
            m.save()

            return HttpResponse("Message Saved!")
        except ObjectDoesNotExist:
            return HttpResponse(
                "Unauthorized! Invalid token. Go to login page",
                status = 401
            )
        except MultipleObjectsReturned:
            return HttpResponse(
                "Unauthorized! Duplicate token. Go to login page",
                status = 401
            )
    else:
        return HttpResponse(
            "Unauthorized! Go to login page",
            status = 401
        )


def chat(request, conversation_id = None):

    if request.user.is_authenticated:
        cm_of_u = ConversationMembers.objects.filter(
            user = request.user
        )
    else:
        return redirect(
            '/users/login'
        )

    messages = []
    if conversation_id:
        c = Conversations.objects.get(
            id = conversation_id
        ) 
        messages = Messages.objects.filter(
            conversation = c
        )
    return render(
        request,
        'chat.html',
        context = {
            'user_conversations': cm_of_u,
            'conversation_id': conversation_id,
            'messages': messages,
        }
    )
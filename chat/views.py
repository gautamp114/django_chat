from django.shortcuts import render

from django.contrib.auth.models import User

from chat.models import Message, Contact, Chat

from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404

from django.db.models import Q

# from django.contrib.auth.decorators import login_required
from .models import Chat

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

# @login_required
def room(request, room_name):
	users = User.objects.all().exclude(username = request.user)
	users_length = User.objects.all().count()

	context = {
		'username': request.user.username,
		'room_name': room_name,
		'users': users,
		'users_length': users_length
	}


	template = 'chat/chat.html'

	return render(request, template, context)


def last_10_messages(chatId):
	chat = get_object_or_404(Chat, id=chatId)
	return chat.messages.all().order_by('-timestamp')[:10][::-1]


def get_msg_contact(username):
	author = User.objects.get(username= username)
	contact_user = get_object_or_404(Contact, user= author)
	return contact_user


def get_chat(chatId):
	return get_object_or_404(Chat, id = chatId)

@csrf_exempt
def ajaxify(request):
	if request.is_ajax():
		user1 = request.user
		param = request.POST['id']
		user2 = User.objects.get(id=param)
		contact_user1 = Contact.objects.get(user=user1)
		contact_user2 = Contact.objects.get(user=user2)

		chatId = Chat.objects.filter(participants=contact_user1).filter(participants=contact_user2).first()

		if chatId == None:
			chat = Chat()
			chat.save()
			chat.participants.add(contact_user1)
			chat.participants.add(contact_user2)
			
			chatId = Chat.objects.filter(participants=contact_user1).filter(participants=contact_user2).first()
			
		context = {
			'chatId': chatId.id
		}
		return JsonResponse(context)
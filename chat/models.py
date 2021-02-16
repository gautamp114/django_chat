from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
	author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		return self.author.username


	# def last_30_message(self):
	# 	return Message.objects.order_by('-timestamp')[:30]


		# latest_chats_list = Chat.objects.order_by('-timestamp')[:10]
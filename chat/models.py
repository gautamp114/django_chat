from django.db import models

from django.contrib.auth.models import User



class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
	friends = models.ManyToManyField('self', blank=True)

	def __str__(self):
		return self.user.username



class Message(models.Model):
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="messages", blank=True)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		return self.contact.user.username



class Chat(models.Model):
	participants = models.ManyToManyField(Contact,related_name='chats')
	messages = models.ManyToManyField(Message, blank=True)


	def __str__(self):
		return "{}".format(self.pk)
		
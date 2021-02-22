from django.contrib import admin
from chat.models import Message,Contact,Chat
# Register your models here.


admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(Chat)
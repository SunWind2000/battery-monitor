from django.contrib import admin
from system.models import System, Battery, Message, Notice

# Register your models here.
admin.site.register(System)
admin.site.register(Battery)
admin.site.register(Message)
admin.site.register(Notice)
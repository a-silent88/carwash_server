from django.contrib import admin

# Register your models here.
from .models import Terminal, Session, Status, StatusTerminal
admin.site.register(Terminal)
admin.site.register(Session)
admin.site.register(Status)
admin.site.register(StatusTerminal)
from django.forms import ModelForm
from .models import Terminal, StatusTerminal, Session


class TerminalForm(ModelForm):

    def __init__(self, *args, **kargs):
        super(TerminalForm, self).__init__(*args, **kargs)
        count = StatusTerminal.objects.all().count()
        if count == 0:
            status_term = StatusTerminal
            status_term.objects.create(
                name='Активен'
            )
            status_term.objects.create(
                name='Не активен'
            )

    class Meta:
        model = Terminal
        fields = ('terminalId', 'name', 'status', 'balance', 'ipAddress')


class SessionForm(ModelForm):

    class Meta:
        model = Session
        fields = ('sessionId', 'terminalId', 'status', 'clientId', 'service', 'balance')

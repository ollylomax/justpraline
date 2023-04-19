from django.contrib import admin
from .models import Messages


class MessagesAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)

    fields = (
        'user', 'date', 'first_name',
        'last_name', 'email', 'subject',
        'message',
        )

    list_display = (
        'user', 'date', 'first_name',
        'last_name', 'email', 'subject',
        )


admin.site.register(Messages, MessagesAdmin)

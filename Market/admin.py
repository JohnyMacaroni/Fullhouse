from asyncio import transports
from django.contrib import admin
from .models import transaction, Info, Global_Info
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(transaction)
#admin.site.register(Message)
admin.site.register(Info)
admin.site.register(Global_Info)

class Information_Info_Inline(admin.StackedInline):
    model = Info
    can_delete = False
    verbose_name_plural = 'information'

class Information_transaction_Inline(admin.StackedInline):
    model = transaction
    can_delete = True
    verbose_name_plural = 'transaction'

class UserAdmin(BaseUserAdmin):
    inlines = (Information_Info_Inline,Information_transaction_Inline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
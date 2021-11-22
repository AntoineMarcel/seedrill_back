from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import *

class EmailModelAdmin(OrderedModelAdmin):
    list_display = ('model', 'order', 'move_up_down_links')
class PersonAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email')
    readonly_fields=('friendCode',)

admin.site.register(EmailModel, EmailModelAdmin)
admin.site.register(Sequence)
admin.site.register(Person, PersonAdmin)

# Register your models here.

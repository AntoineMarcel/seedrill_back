from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import *

class EmailModelAdmin(OrderedModelAdmin):
    list_display = ('model', 'order', 'move_up_down_links')

admin.site.register(EmailModel, EmailModelAdmin)
admin.site.register(Sequence)
admin.site.register(Person)

# Register your models here.

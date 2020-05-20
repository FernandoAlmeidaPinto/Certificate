from django.contrib import admin
from .models import FormInformation, Certificate

# Register your models here.

class FormInfoAdmin(admin.ModelAdmin):
    list_display = ('event', 'date', 'date_creaded')

admin.site.register(FormInformation, FormInfoAdmin)
admin.site.register(Certificate)
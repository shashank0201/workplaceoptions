from django.contrib import admin

# Register your models here.
from . models import Person

class PersonAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ('name','email', 'phone')

admin.site.register(Person, PersonAdmin)
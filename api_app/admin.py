from django.contrib import admin
from .models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords


admin.site.register(Sites)
admin.site.register(Log)
admin.site.register(Pages)
admin.site.register(Persons)
admin.site.register(PersonsPageRank)
admin.site.register(KeyWords)
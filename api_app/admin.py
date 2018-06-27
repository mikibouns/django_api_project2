from django.contrib import admin
from .models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords
from auth_app.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['addedBy', ]


admin.site.register(Sites)
admin.site.register(Log)
admin.site.register(Pages)
admin.site.register(Persons)
admin.site.register(PersonsPageRank)
admin.site.register(KeyWords)
admin.site.register(User, UserAdmin)

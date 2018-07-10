from django.contrib import admin
from .models import Sites, Log, Pages, Persons, PersonsPageRank, KeyWords
from auth_app.models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['addedBy', ]


class LogAdmin(admin.ModelAdmin):
    list_filter = ('method', 'addedBy', 'status_code', 'action', 'logDate')

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(Sites)
admin.site.register(Log, LogAdmin)
admin.site.register(Pages)
admin.site.register(Persons)
admin.site.register(PersonsPageRank)
admin.site.register(KeyWords)
admin.site.register(User, UserAdmin)

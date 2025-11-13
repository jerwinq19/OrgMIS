from django.contrib import admin
from .models import Document, Organization, Events, CustomUser, Budget, EventAttendance

admin.site.register(Events)
admin.site.register(Document)
admin.site.register(Organization)
admin.site.register(CustomUser)
admin.site.register(Budget)
admin.site.register(EventAttendance)

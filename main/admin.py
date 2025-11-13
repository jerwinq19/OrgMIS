from django.contrib import admin
from .models import Document, Organization, Events, CustomUser, Budget, EventAttendance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = CustomUser
    # Override fieldsets to only include existing fields
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'user_type', 'position', 'organization')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'position', 'organization', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    list_display = ('username', 'email', 'user_type', 'position', 'organization', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'user_type', 'position', 'organization')
    ordering = ('username',)
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Events)
admin.site.register(Document)
admin.site.register(Organization)
admin.site.register(Budget)
admin.site.register(EventAttendance)

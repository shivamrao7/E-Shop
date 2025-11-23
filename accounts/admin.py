from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, UserProfile

class AccountAdmin(UserAdmin):
    list_display = ['profile_image', 'email', 'full_name', 'username', 'is_staff', 'is_active', 'status_badge', 'join_date']
    readonly_fields = ['date_joined_for_format', 'last_login_for_format']
    ordering = ('-date_joined_for_format',)
    list_filter = ['is_active', 'is_staff', 'is_superadmin']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_per_page = 25
    actions = ['make_active', 'make_inactive', 'make_staff', 'revoke_staff']
    
    def profile_image(self, obj):
        return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{}</div>', obj.first_name[:1] if obj.first_name else obj.email[:1].upper())
    profile_image.short_description = 'Avatar'
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else "No Name"
    full_name.short_description = 'Full Name'
    
    def status_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">SUPERUSER</span>')
        elif obj.is_staff:
            return format_html('<span style="background: #ffc107; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">STAFF</span>')
        elif obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">ACTIVE</span>')
        return format_html('<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">INACTIVE</span>')
    status_badge.short_description = 'Status'
    
    def join_date(self, obj):
        return obj.date_joined_for_format.strftime('%Y-%m-%d')
    join_date.short_description = 'Joined'
    
    filter_horizontal = ()
    fieldsets = ()

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) marked active.")
    make_active.short_description = 'Mark selected users as active'

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) marked inactive.")
    make_inactive.short_description = 'Mark selected users as inactive'

    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} user(s) granted staff status.")
    make_staff.short_description = 'Grant staff status to selected users'

    def revoke_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"{updated} user(s) revoked staff status.")
    revoke_staff.short_description = 'Revoke staff status for selected users'

admin.site.register(Account, AccountAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_thumbnail', 'user_info', 'location']
    list_filter = ['country', 'state']
    search_fields = ['user__email', 'user__first_name', 'city']
    
    def profile_thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
        return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">{}</div>', obj.user.first_name[:1] if obj.user.first_name else obj.user.email[:1].upper())
    profile_thumbnail.short_description = 'Profile'
    
    def user_info(self, obj):
        return format_html('<strong>{}</strong><br><small>{}</small>', 
                          f"{obj.user.first_name} {obj.user.last_name}" if obj.user.first_name else obj.user.username,
                          obj.user.email)
    user_info.short_description = 'User'
    
    def location(self, obj):
        location_parts = [obj.city, obj.state, obj.country]
        location = ", ".join([part for part in location_parts if part])
        return location if location else "Not specified"
    location.short_description = 'Location'


# Site branding for admin (applies at import time)
admin.site.site_header = 'E-Shop Administration'
admin.site.site_title = 'E-Shop Admin'
admin.site.index_title = 'Welcome to E-Shop Admin'

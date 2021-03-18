from django.contrib import admin

from padmin.models import UserIP, DayNumber


@admin.register(UserIP)
class IPAdmin(admin.ModelAdmin):
    readonly_fields = ['account', 'ip', 'ip_addr', 'character']

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DayNumber)
class DayAdmin(admin.ModelAdmin):
    readonly_fields = ['day', 'user', 'count']

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

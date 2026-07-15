from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BaseModelAdmin(admin.ModelAdmin):
    """
    Base admin class for all business models in the project.
    
    Provides automatic handling for:
    - UUID primary keys (readonly)
    - Created/Updated timestamps (readonly, date hierarchy)
    - Soft delete functionality (if the mixin is applied)
    """
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_display = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically add 'deleted_at' to readonly fields 
        only if the model actually has a soft-delete field.
        """
        fields = super().get_readonly_fields(request, obj)
        if hasattr(self.model, 'deleted_at'):
            fields = list(fields) + ['deleted_at']
        return fields

    def get_actions(self, request):
        """
        Remove the default 'delete_selected' action if the model uses soft-delete,
        and replace it with a custom 'soft_delete_selected' action.
        """
        actions = super().get_actions(request)
        if hasattr(self.model, 'soft_delete'):
            if 'delete_selected' in actions:
                del actions['delete_selected']
            actions['soft_delete_selected'] = (
                self.soft_delete_selected,
                'soft_delete_selected',
                _("Soft delete selected items")
            )
        return actions

    def soft_delete_selected(self, request, queryset):
        """Bulk soft-delete action"""
        queryset.update(is_deleted=True, deleted_at=timezone.now())
    soft_delete_selected.short_description = _("Soft delete selected items")
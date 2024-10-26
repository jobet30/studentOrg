from django.contrib import admin
from .models import SubmittedForm

class SubmittedFormAdmin(admin.ModelAdmin):
    list_display = ('user', 'form_title', 'created_at', 'is_reviewed', 'reviewed_at', 'admin_comments')
    list_filter = ('is_reviewed', 'created_at', 'reviewed_at')
    search_fields = ('user__username', 'form_title')
    readonly_fields = ('created_at', 'reviewed_at')
    ordering = ('-created_at',)

admin.site.register(SubmittedForm, SubmittedFormAdmin)
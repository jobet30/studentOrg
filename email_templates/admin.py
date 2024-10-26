from django.contrib import admin
from .models import EmailTemplates

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo_preview', 'created_at', 'updated_at')  # Display these fields in the list view
    search_fields = ('name',) 
    list_filter = ('created_at',)

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="width: 50px; height: auto;" />')
        return "-"
    logo_preview.short_description = 'Logo Preview' 

admin.site.register(EmailTemplates, EmailTemplateAdmin)
from django.contrib import admin
from .models import User, Profile, Skill, Role, Verification, MentorRequest

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

admin.site.register(User, UserAdmin)
admin.site.register(Skill)
admin.site.register(Role)
admin.site.register(Verification)
admin.site.register(MentorRequest)
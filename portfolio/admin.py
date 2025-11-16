from django.contrib import admin
from django.utils.html import format_html
from .models import Skill, Project, Experience, Contact, SiteVisit, SiteSettings

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['order', 'proficiency']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'featured', 'views', 'created_at', 'image_preview']
    list_filter = ['status', 'featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['featured', 'status']
    filter_horizontal = ['technologies']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Aperçu"

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'current']
    list_filter = ['current', 'start_date']
    search_fields = ['company', 'position']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'company', 'subject', 'priority_badge', 'created_at', 'read', 'replied']
    list_filter = ['read', 'replied', 'priority', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
    list_editable = ['read', 'replied']
    readonly_fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'priority', 
                      'project_budget', 'created_at', 'ip_address', 'user_agent']
    
    fieldsets = (
        ('Informations de contact', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'priority', 'project_budget')
        }),
        ('Gestion', {
            'fields': ('read', 'replied', 'reply_message', 'replied_at')
        }),
        ('Informations techniques', {
            'fields': ('created_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_badge(self, obj):
        colors = {
            'low': '#28a745',
            'medium': '#17a2b8', 
            'high': '#ffc107',
            'urgent': '#dc3545'
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = "Priorité"

@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'page', 'timestamp']
    list_filter = ['timestamp', 'page']
    search_fields = ['ip_address', 'page']
    readonly_fields = ['ip_address', 'user_agent', 'page', 'timestamp', 'session_key']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('name', 'tagline', 'bio', 'profile_image')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Réseaux sociaux', {
            'fields': ('github', 'linkedin', 'whatsapp')
        }),
        ('Documents', {
            'fields': ('resume_file',)
        }),
    )
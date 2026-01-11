from django.contrib import admin
from .models import Document, Article, Volunteer, Donation, Newsletter, DocumentLocation, DocumentLocationAssignment


@admin.register(DocumentLocation)
class DocumentLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    readonly_fields = ('slug',)
    fields = ('slug', 'name', 'description')


class DocumentLocationAssignmentInline(admin.TabularInline):
    model = DocumentLocationAssignment
    extra = 1
    fields = ('location', 'order')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'priority', 'get_locations')
    list_filter = ('uploaded_at', 'priority')
    search_fields = ('title', 'extracted_text')
    readonly_fields = ('uploaded_at', 'extracted_text')
    
    fieldsets = (
        ('Document Info', {
            'fields': ('title', 'file', 'uploaded_at')
        }),
        ('Display Settings', {
            'fields': ('description', 'priority')
        }),
        ('Content', {
            'fields': ('extracted_text',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [DocumentLocationAssignmentInline]
    
    def get_locations(self, obj):
        locations = obj.locations.all()
        return ', '.join([loc.name for loc in locations]) if locations else 'None'
    get_locations.short_description = 'Placements'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published', 'created_at')
    list_filter = ('published', 'category', 'created_at')
    search_fields = ('title', 'content')
    fieldsets = (
        ('Article Info', {
            'fields': ('title', 'description', 'category')
        }),
        ('Content', {
            'fields': ('content', 'pdf_url')
        }),
        ('Publishing', {
            'fields': ('published',)
        }),
    )


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'joined_at')
    list_filter = ('status', 'joined_at')
    search_fields = ('name', 'email')
    readonly_fields = ('joined_at',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'amount', 'created_at')
    list_filter = ('amount', 'created_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

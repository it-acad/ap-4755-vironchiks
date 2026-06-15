from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'display_authors')
    list_filter = ('id', 'name', 'authors')

    fieldsets = (
        ('Data that do not change', {
            'fields': ('name', 'description', 'authors'),
        }),
        ('Data that change', {
            'fields': ('count',),
        }),
    )

    def display_authors(self, obj):
        return ", ".join([f"{author.name} {author.surname}" for author in obj.authors.all()])
    
    display_authors.short_description = 'Authors'
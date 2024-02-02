from django.contrib import admin
from .models import Todo, Category

# Register your models here.

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'user', 'category']
    list_filter = ['title', 'user', 'completed', 'category']
admin.site.register(Category)

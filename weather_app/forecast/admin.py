from django.contrib import admin
from .models import City, SearchHistory

# admin.site.register(City)
# admin.site.register(SearchHistory)


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    last_display = ('name', 'search_count')
    search_fields = ('name',)
    ordering = ('-search_count',)
    
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    last_display = ('name', 'user', 'session_key', 'search_time')
    last_filer = ('search_time', 'city')
    search_fields = ('city__name', 'user__username')
    ordering = ('-search_time',)
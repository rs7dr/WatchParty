from django.contrib import admin
from .models import MyUser, Event


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['event_name']}),
        (None, {'fields': ['event_date']}),
        (None, {'fields': ['event_time']}),
        (None, {'fields': ['event_location']}),
        (None, {'fields': ['event_type']}),
        (None, {'fields': ['event_description']}),
        (None, {'fields': ['event_owner']}),
        (None, {'fields': ['event_RSVP']}),
        ('Post date', {'fields': ['event_post_date']})
    ]
    list_display = ('event_name', 'event_owner', 'event_post_date')
    list_filter = ['event_date']
    search_fields = ['event_name', 'event_owner']

# Display on site
admin.site.register(MyUser)
admin.site.register(Event, EventAdmin)
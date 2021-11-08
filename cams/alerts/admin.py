from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from base64 import b64encode
import datetime 
from .models import Alert, Detect


class AlertsAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        decoded = b64encode(obj.snapshot).decode('utf-8')
        imgtag = '<img class="thumbnail" src="data:image/jpeg;base64, {}" width="150"/>'.format(decoded)
        return format_html(imgtag)

    image_tag.short_description = 'Image'

    def time_seconds(self, obj):
        if obj.timestamp:
            ts = obj.timestamp
        else:
            ts = datetime.datetime.now()
        return ts.strftime("%Y-%m-%d %H:%M:%S")

    time_seconds.short_description = 'Timestamp' 

    list_display = ('subject', 'time_seconds', 'image_tag')
    list_filter = ('timestamp',)
    change_list_template = 'admin/alerts/alarm_change_list.html'


class DetectsAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        decoded = b64encode(obj.snapshot).decode('utf-8')
        imgtag = '<img class="thumbnail" src="data:image/jpeg;base64, {}" width="150"/>'.format(decoded)
        return format_html(imgtag)

    image_tag.short_description = 'Image'

    def time_seconds(self, obj):
        if obj.timestamp:
            ts = obj.timestamp
        else:
            ts = datetime.datetime.now()
        return ts.strftime("%Y-%m-%d %H:%M:%S")

    time_seconds.short_description = 'Timestamp' 

    list_display = ('subject', 'time_seconds', 'image_tag')
    list_filter = ('timestamp',)
    change_list_template = 'admin/detects/detect_change_list.html'


admin.site.site_header = 'Surveillance Camera Alerts Administration'
admin.site.unregister(Group) 
admin.site.register(Alert, AlertsAdmin)
admin.site.register(Detect, DetectsAdmin)




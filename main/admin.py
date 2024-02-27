from django.contrib import admin

from main.models import *

class CourseAdmin(admin.ModelAdmin):
    list_display=("name", "date_created", "date_modified")

admin.site.register(Course, CourseAdmin)
admin.site.register(ClassSchedule)
admin.site.register(ClassAttendance)
admin.site.register(Query)
admin.site.register(QueryComment)
from django.contrib import admin

from notice_board.models import Guild, Meeting, Sphere

admin.site.register(Guild)
admin.site.register(Sphere)
admin.site.register(Meeting)

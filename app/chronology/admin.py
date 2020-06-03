from django.contrib import admin

from chronology.models import (
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    TimeTable,
    WaitList,
)

admin.site.register(Festival)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(Helper)
admin.site.register(TimeTable)
admin.site.register(WaitList)
admin.site.register(Proposal)

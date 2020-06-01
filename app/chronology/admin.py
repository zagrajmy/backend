from django.contrib import admin
from chronology.models import (
    Festival,
    Room,
    TimeSlot,
    Helper,
    TimeTable,
    WaitList,
    Proposal,
)


admin.site.register(Festival)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(Helper)
admin.site.register(TimeTable)
admin.site.register(WaitList)
admin.site.register(Proposal)

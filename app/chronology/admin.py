from django.contrib import admin

from chronology.models import (
    AgendaItem,
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    WaitList,
)

admin.site.register(Festival)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(Helper)
admin.site.register(AgendaItem)
admin.site.register(WaitList)
admin.site.register(Proposal)

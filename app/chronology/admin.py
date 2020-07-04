from chronology.models import (
    AgendaItem,
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    WaitList,
)
from django.contrib import admin
from notice_board.admin import SphereManagersAdmin

admin.site.register(AgendaItem, SphereManagersAdmin)
admin.site.register(Festival, SphereManagersAdmin)
admin.site.register(Helper, SphereManagersAdmin)
admin.site.register(Proposal, SphereManagersAdmin)
admin.site.register(Room, SphereManagersAdmin)
admin.site.register(TimeSlot, SphereManagersAdmin)
admin.site.register(WaitList, SphereManagersAdmin)

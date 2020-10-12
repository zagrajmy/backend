from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TypedDict, Union

from .models import AgendaItem, TimeSlot

UnassignedMeeting = TypedDict(
    "UnassignedMeeting", {"pk": int, "name": str, "proposal__time_slots": int}
)


class AgendaCellDict(TypedDict):
    room: str
    item: Optional[Union[AgendaItem, List[UnassignedMeeting]]]
    rowspan: int


class AgendaMatrixRow(TypedDict):
    hour: datetime
    items: List[Optional[AgendaCellDict]]


class RoomInfo(TypedDict):
    name: str
    pk: int


class AgendaBuilder:
    def __init__(
        self,
        agenda_items: List[AgendaItem],
        rooms: List[RoomInfo],
        time_slots: List[TimeSlot],
        unassigned_meetings: List[UnassignedMeeting],
    ) -> None:
        self._agenda_items = {
            (item.room.name, item.meeting.start_time): item for item in agenda_items
        }
        self._agenda_matrix: List[AgendaMatrixRow] = []
        self._rooms = rooms
        self._rowspans = [0] * len(self._rooms)
        self._times = self._get_times(time_slots)
        self._unassigned_meetings = self._unassigned_meetings_by_time_slot(
            unassigned_meetings
        )

    def build(self) -> None:
        for time_slot, times in self._times.items():

            for hour in times:
                matrix_row: AgendaMatrixRow = {"hour": hour, "items": []}
                for i, room in enumerate(self._rooms):
                    item = None if self._rowspans[i] else self._get_item(i, room, hour)
                    matrix_row["items"].append(item)
                    self._rowspans[i] = max(self._rowspans[i] - 1, 0)
                if hour == times[0]:
                    matrix_row["items"].append(
                        {
                            "room": "unassigned",
                            "item": self._unassigned_meetings[time_slot.pk],
                            "rowspan": len(times),
                        }
                    )
                self._agenda_matrix.append(matrix_row)

    def _get_item(self, i: int, room: RoomInfo, hour: datetime) -> AgendaCellDict:
        rowspan = 1
        agenda_item = self._agenda_items.get((room["name"], hour), None)
        if agenda_item:
            duration = agenda_item.meeting.proposal.duration_minutes
            self._agenda_items.pop((room["name"], hour))
            if duration >= 30:
                rowspan = duration // 30
                self._rowspans[i] = rowspan
            else:
                agenda_item = None
        return {"room": room["name"], "item": agenda_item, "rowspan": rowspan}

    @property
    def agenda_matrix(self) -> List[AgendaMatrixRow]:
        return self._agenda_matrix

    @property
    def broken_agenda_items(self) -> List[AgendaItem]:
        return list(self._agenda_items.values())

    @staticmethod
    def _get_times(
        time_slots: List[TimeSlot],
    ) -> Dict[TimeSlot, List[datetime]]:
        times = {}
        for time_slot in time_slots:
            number = (time_slot.end_time - time_slot.start_time).total_seconds() / 1800
            times[time_slot] = [
                time_slot.start_time + timedelta(seconds=i * 1800)
                for i in range(int(number))
            ]
        return times

    @staticmethod
    def _unassigned_meetings_by_time_slot(
        unassigned_meetings: List[UnassignedMeeting],
    ) -> Dict[int, List[UnassignedMeeting]]:
        by_time_slot = defaultdict(list)
        for meeting in unassigned_meetings:
            by_time_slot[meeting["proposal__time_slots"]].append(meeting)
        return by_time_slot

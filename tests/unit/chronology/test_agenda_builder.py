from dataclasses import dataclass
from datetime import datetime

from chronology.agenda_builder import AgendaBuilder


@dataclass(frozen=True)
class DummyProposal:
    duration_minutes: int


@dataclass(frozen=True)
class DummyMeeting:
    start_time: datetime
    proposal: DummyProposal = None


@dataclass(frozen=True)
class DummyAgendaItem:
    room: str
    meeting: DummyMeeting


@dataclass(frozen=True)
class DummyTimeSlot:
    start_time: datetime
    end_time: datetime
    pk: int


def test_init_empty():
    agenda_builder = AgendaBuilder(
        agenda_items=[], rooms=[], time_slots=[], unassigned_meetings=[]
    )

    assert agenda_builder.agenda_matrix == []
    assert agenda_builder.broken_agenda_items == []


def test_init(hour):
    agenda_items = [
        DummyAgendaItem(room="1", meeting=DummyMeeting(start_time=hour(0))),
        DummyAgendaItem(room="2", meeting=DummyMeeting(start_time=hour(0))),
        DummyAgendaItem(room="3", meeting=DummyMeeting(start_time=hour(0))),
        DummyAgendaItem(room="4", meeting=DummyMeeting(start_time=hour(0))),
    ]

    agenda_builder = AgendaBuilder(
        agenda_items=agenda_items, rooms=[], time_slots=[], unassigned_meetings=[]
    )

    assert agenda_builder.agenda_matrix == []
    assert agenda_builder.broken_agenda_items == agenda_items


def test_init_build(hour):
    agenda_items = [
        DummyAgendaItem(
            room="A1",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=30), start_time=hour(-7)
            ),
        ),
        DummyAgendaItem(
            room="A1",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=30), start_time=hour(0)
            ),
        ),
        DummyAgendaItem(
            room="A1",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=30), start_time=hour(6)
            ),
        ),
        DummyAgendaItem(
            room="A2",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=30), start_time=hour(0)
            ),
        ),
        DummyAgendaItem(
            room="B2",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=30), start_time=hour(-4)
            ),
        ),
        DummyAgendaItem(
            room="A2",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=420), start_time=hour(-4)
            ),
        ),
        DummyAgendaItem(
            room="B2",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=120), start_time=hour(-5)
            ),
        ),
        DummyAgendaItem(
            room="B1",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=60), start_time=hour(3)
            ),
        ),
        DummyAgendaItem(
            room="A1",
            meeting=DummyMeeting(
                proposal=DummyProposal(duration_minutes=15), start_time=hour(3)
            ),
        ),
    ]
    time_slots = [
        DummyTimeSlot(pk=1, start_time=hour(-6), end_time=hour(-3)),
        DummyTimeSlot(pk=2, start_time=hour(2), end_time=hour(5)),
    ]
    agenda_builder = AgendaBuilder(
        agenda_items=agenda_items,
        rooms=["A1", "A2", "B1", "B2"],
        time_slots=time_slots,
        unassigned_meetings=[
            {
                "pk": 1,
                "name": "Meeting 1",
                "proposal__time_slots": 1,
            },
            {
                "pk": 2,
                "name": "Meeting 2",
                "proposal__time_slots": 1,
            },
            {
                "pk": 2,
                "name": "Meeting 2",
                "proposal__time_slots": 2,
            },
        ],
    )

    agenda_builder.build()

    assert agenda_builder.agenda_matrix == [
        {
            "hour": hour(-6),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                {"item": None, "room": "A2", "rowspan": 1},
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
                {
                    "item": [
                        {"name": "Meeting 1", "pk": 1},
                        {"name": "Meeting 2", "pk": 2},
                    ],
                    "room": "unassigned",
                    "rowspan": 6,
                },
            ],
        },
        {
            "hour": hour(-5.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                {"item": None, "room": "A2", "rowspan": 1},
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
        {
            "hour": hour(-5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                {"item": None, "room": "A2", "rowspan": 1},
                {"item": None, "room": "B1", "rowspan": 1},
                {
                    "item": DummyAgendaItem(
                        room="B2",
                        meeting=DummyMeeting(
                            start_time=hour(-5),
                            proposal=DummyProposal(duration_minutes=120),
                        ),
                    ),
                    "room": "B2",
                    "rowspan": 4,
                },
            ],
        },
        {
            "hour": hour(-4.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                {"item": None, "room": "A2", "rowspan": 1},
                {"item": None, "room": "B1", "rowspan": 1},
                None,
            ],
        },
        {
            "hour": hour(-4),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                {
                    "item": DummyAgendaItem(
                        room="A2",
                        meeting=DummyMeeting(
                            start_time=hour(-4),
                            proposal=DummyProposal(duration_minutes=420),
                        ),
                    ),
                    "room": "A2",
                    "rowspan": 14,
                },
                {"item": None, "room": "B1", "rowspan": 1},
                None,
            ],
        },
        {
            "hour": hour(-3.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {"item": None, "room": "B1", "rowspan": 1},
                None,
            ],
        },
        {
            "hour": hour(2),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
                {
                    "item": [{"name": "Meeting 2", "pk": 2}],
                    "room": "unassigned",
                    "rowspan": 6,
                },
            ],
        },
        {
            "hour": hour(2.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
        {
            "hour": hour(3),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {
                    "item": DummyAgendaItem(
                        room="B1",
                        meeting=DummyMeeting(
                            start_time=hour(3),
                            proposal=DummyProposal(duration_minutes=60),
                        ),
                    ),
                    "room": "B1",
                    "rowspan": 2,
                },
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
        {
            "hour": hour(3.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                None,
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
        {
            "hour": hour(4),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
        {
            "hour": hour(4.5),
            "items": [
                {"item": None, "room": "A1", "rowspan": 1},
                None,
                {"item": None, "room": "B1", "rowspan": 1},
                {"item": None, "room": "B2", "rowspan": 1},
            ],
        },
    ]
    assert agenda_builder.broken_agenda_items == agenda_items[:-4]

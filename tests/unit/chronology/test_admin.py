from unittest.mock import Mock

import pytest
from django.utils.text import slugify

from chronology.admin import (
    AgendaItemAdmin,
    AgendaItemForm,
    FestivalAdmin,
    ProposalAdmin,
)
from chronology.models import AgendaItem, Festival, Proposal, TimeSlot
from notice_board.models import Meeting
from tests.factories import (
    AgendaItemFactory,
    FestivalFactory,
    HelperFactory,
    MeetingFactory,
    ProposalFactory,
    RoomFactory,
    SphereFactory,
    UserFactory,
)


@pytest.fixture
def agenda_item_admin():
    admin_site = Mock()
    admin_site._registry.get().get_ordering.return_value = ["id"]
    return AgendaItemAdmin(model=AgendaItem, admin_site=admin_site)


@pytest.fixture
def proposal_admin():
    return ProposalAdmin(model=Proposal, admin_site=Mock())


@pytest.fixture
def request_with_user():
    request = Mock()
    current_user = UserFactory()
    request.user = current_user
    return request


@pytest.fixture
def festival_admin():
    agenda_builder_class_mock = Mock()
    agenda_builder_class_mock().agenda_matrix = "matrix123"
    agenda_builder_class_mock().broken_agenda_items = "broken321"
    admin_site_mock = Mock()
    admin_site_mock.each_context.return_value = {"self": "a456"}
    FestivalAdmin.agenda_builder_class = agenda_builder_class_mock
    yield FestivalAdmin(model=Festival, admin_site=admin_site_mock)
    agenda_builder_class_mock().build.assert_called()


@pytest.fixture
def request_builder(hour):
    def _build_request(room_id, popup=None):
        request = Mock()
        request.GET = {
            "hour": hour(2).strftime("%Y-%m-%d-%H-%M-%S-%f-%Z"),
            "room": room_id,
        }
        if popup:
            request.GET["_popup"] = 1
        return request

    return _build_request


@pytest.fixture
def festival_room(hour):
    def _build_room(start, end):
        room = RoomFactory()
        time_slot = room.festival.time_slots.last()
        time_slot.start_time = hour(start)
        time_slot.end_time = hour(end)
        time_slot.save()
        return room

    return _build_room


def _get_meeting_fields_from_proposal(proposal, organizer=None, slug=None):
    return (
        ("description", proposal.description),
        ("id", proposal.meeting.id),
        ("name", proposal.name),
        ("organizer", organizer or proposal.speaker_user),
        ("publication_time", proposal.waitlist.festival.start_publication),
        ("slug", slug or slugify(proposal.name)[:48]),
        ("sphere", proposal.waitlist.festival.sphere),
    )


def _check_agenda_form(room, expected, errors, **kwargs):
    proposal = ProposalFactory(
        waitlist__festival=room.festival, duration_minutes=8, **kwargs
    )

    form = AgendaItemForm(
        data={
            "hour": "2020-08-01-10-00-00-000000-UTC",
            "meeting": proposal.meeting,
            "room": room,
        }
    )

    assert form.is_valid() is expected
    assert form.errors == errors


@pytest.mark.django_db
def test_accept_proposals(proposal_admin, request_with_user):
    proposals = []
    for i in range(10):
        proposal = ProposalFactory()
        if i % 2 == 0:
            proposal.meeting = None
            proposal.save()
            proposals.append(proposal)

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    for proposal in Proposal.objects.filter(id__in=[p.id for p in proposals]):
        for field, value in _get_meeting_fields_from_proposal(proposal):
            assert getattr(proposal.meeting, field) == value
    request_with_user._messages.add.assert_called_once_with(
        20, "Total processed: 10, accepted: 5", ""
    )


@pytest.mark.parametrize(
    "name,new_slug,kwargs",
    (
        ("Slug 123", "slug-123-1", {"slug": "slug-123"}),
        ("q" * 56, "q" * 48 + "-1", {"slug": "q" * 48}),
        ("q" * 56, "q" * 48, {"slug": None}),
        ("Slug 123", "slug-123", {"organizer": True}),
    ),
)
@pytest.mark.django_db
def test_accept_proposals_duplicate_slug(
    proposal_admin, request_with_user, name, new_slug, kwargs
):
    sphere = SphereFactory()
    if kwargs.get("slug"):
        MeetingFactory(slug=kwargs.get("slug"), sphere=sphere)
    proposal = ProposalFactory(
        meeting=None, name=name, waitlist__festival__sphere=sphere
    )
    if kwargs.get("organizer"):
        proposal.speaker_user = None
        proposal.save()

    proposal_admin.accept_proposals(
        request=request_with_user, queryset=Proposal.objects.order_by("id")
    )

    proposal = Proposal.objects.last()
    organizer = (
        request_with_user.user if kwargs.get("organizer") else proposal.speaker_user
    )
    for field, value in _get_meeting_fields_from_proposal(
        proposal, slug=new_slug, organizer=organizer
    ):
        assert getattr(proposal.meeting, field) == value


@pytest.mark.django_db
def test_festival_agenda(festival_admin):
    festival = FestivalFactory()

    response = festival_admin.agenda(Mock(), festival.id)

    assert response.template_name == "chronology/agenda.html"
    context = dict(response.context_data)
    context.pop("media")
    assert context == {
        "self": "a456",
        "festival": festival,
        "title": f"Festival schedule {festival.name}",
        "agenda_matrix": "matrix123",
        "broken_agenda_items": "broken321",
    }


@pytest.mark.parametrize(
    "start_time,end_time,expected,errors",
    (
        (-2, -1, True, {}),
        (-2, 0, True, {}),
        (
            -2,
            1,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (
            -2,
            1,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (
            0,
            1,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (
            1,
            2,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (
            1,
            4,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (
            1,
            5,
            False,
            {"__all__": ["There's already an agenda item in this time slot."]},
        ),
        (4, 5, True, {}),
        (5, 7, True, {}),
    ),
)
@pytest.mark.django_db
def test_agenda_item_form(hour, festival_room, start_time, end_time, expected, errors):
    room = festival_room(-3, 8)

    AgendaItemFactory(
        meeting__created_at=hour(-6),
        meeting__end_time=hour(end_time),
        meeting__publication_time=hour(-4),
        meeting__start_time=hour(start_time),
        room=room,
    )

    _check_agenda_form(room, expected, errors)


@pytest.mark.django_db
def test_agenda_item_form_wrong_timeslot(festival_room):
    room = festival_room(-1, 3)

    _check_agenda_form(
        room, False, {"__all__": ["Meeting too long for this time slot and hour"]}
    )


@pytest.mark.django_db
def test_agenda_item_form_update(hour, festival_room):
    room = festival_room(-3, 8)
    agenda_item = AgendaItemFactory(
        room=room,
        meeting__start_time=hour(-2),
        meeting__end_time=hour(2),
        meeting__publication_time=hour(-4),
    )
    proposal = ProposalFactory(
        meeting=MeetingFactory(), waitlist__festival=room.festival, duration_minutes=8,
    )

    form = AgendaItemForm(
        instance=agenda_item, data={"meeting": proposal.meeting, "room": room},
    )

    assert form.is_valid() is True


@pytest.mark.parametrize("speaker_field", ("speaker_user", "speaker_name"))
@pytest.mark.django_db
def test_agenda_item_form_speaker_error(hour, festival_room, speaker_field):
    room = festival_room(-3, 8)
    speaker_kwargs = {"speaker_user": None}
    speaker_kwargs[speaker_field] = (
        "Maciek" if speaker_field == "speaker_name" else UserFactory()
    )
    old_proposal = ProposalFactory(
        meeting__created_at=hour(-6),
        meeting__end_time=hour(1),
        meeting__publication_time=hour(-4),
        meeting__start_time=hour(-1),
        **speaker_kwargs,
    )
    AgendaItemFactory(meeting=old_proposal.meeting)

    _check_agenda_form(
        room,
        False,
        {"__all__": ["User already has a meeting at this hour"]},
        **speaker_kwargs,
    )


@pytest.mark.django_db
def test_agenda_item_form_helper_conflict(hour, festival_room):
    helper = HelperFactory()
    AgendaItemFactory(
        helper=helper,
        meeting__created_at=hour(-6),
        meeting__end_time=hour(1),
        meeting__publication_time=hour(-4),
        meeting__start_time=hour(-1),
    )
    room = festival_room(-3, 8)

    _check_agenda_form(
        room,
        False,
        {"__all__": ["User is on helper duty during this time"]},
        speaker_user=helper.user,
    )


@pytest.mark.django_db
def test_agenda_item_no_hour():
    room = RoomFactory()
    proposal = ProposalFactory(waitlist__festival=room.festival, duration_minutes=8)

    form = AgendaItemForm(data={"meeting": proposal.meeting, "room": room})

    assert form.is_valid() is False
    assert form.errors == {"__all__": ["Missing hour field value"]}


@pytest.mark.parametrize("proposal_end_time,expected", ((10, 2), (1, 1)))
@pytest.mark.django_db
def test_agenda_item_admin_get_field_queryset_meeting(
    hour, request_builder, agenda_item_admin, proposal_end_time, expected
):
    AgendaItemFactory()
    room = RoomFactory()
    AgendaItemFactory(room__festival=room.festival)
    agenda_item = AgendaItemFactory(
        room=room,
        meeting__publication_time=hour(1),
        meeting__start_time=hour(2),
        meeting__end_time=hour(3),
    )
    proposal = ProposalFactory(waitlist__festival=room.festival)
    proposal.time_slots.add(
        TimeSlot.objects.create(
            festival=room.festival, start_time=hour(0), end_time=hour(proposal_end_time)
        )
    )
    request = request_builder(room_id=room.id, popup=1)

    queryset = agenda_item_admin.get_field_queryset(
        db=None, db_field=AgendaItem._meta.get_field("meeting"), request=request
    )

    assert queryset.count() == expected
    assert agenda_item.meeting in queryset.all()
    if expected == 2:
        assert proposal.meeting in queryset.all()


@pytest.mark.django_db
def test_agenda_item_admin_get_field_queryset_helper(
    hour, request_builder, agenda_item_admin
):
    HelperFactory()
    festival = FestivalFactory(
        start_proposal=hour(-6),
        end_proposal=hour(-5),
        start_publication=hour(-5),
        start_time=hour(-4),
        end_time=hour(4),
    )
    room = RoomFactory(festival=festival)
    helper2 = HelperFactory(festival=festival)
    helper2.time_slots.add(festival.time_slots.get(start_time__lt=hour()))
    helper = HelperFactory(festival=festival)
    helper.time_slots.add(festival.time_slots.get(start_time__gte=hour()))
    request = request_builder(room_id=room.id, popup=1)

    queryset = agenda_item_admin.get_field_queryset(
        db=None, db_field=AgendaItem._meta.get_field("helper"), request=request
    )

    assert queryset.count() == 1
    assert queryset.last() == helper


@pytest.mark.django_db
def test_agenda_item_admin_get_field_queryset_room(
    hour, request_builder, agenda_item_admin
):
    RoomFactory()
    festival = FestivalFactory()
    room1 = RoomFactory(festival=festival)
    room2 = RoomFactory(festival=festival)
    request = request_builder(room_id=room1.id, popup=1)

    queryset = agenda_item_admin.get_field_queryset(
        db=None, db_field=AgendaItem._meta.get_field("room"), request=request
    )

    assert queryset.count() == 1
    assert room1 in queryset.all()
    assert room2 not in queryset.all()


@pytest.mark.django_db
def test_agenda_item_admin_get_field_queryset_no_request(agenda_item_admin):
    RoomFactory()
    RoomFactory()
    RoomFactory()

    queryset = agenda_item_admin.get_field_queryset(
        db=None, db_field=AgendaItem._meta.get_field("room"), request=None
    )

    assert queryset.count() == 3


@pytest.mark.django_db
def test_agenda_item_admin_get_field_queryset_no_popup(
    hour, agenda_item_admin, request_builder
):
    RoomFactory()
    RoomFactory()
    room = RoomFactory()
    request = request_builder(room_id=room.id)

    queryset = agenda_item_admin.get_field_queryset(
        db=None, db_field=AgendaItem._meta.get_field("room"), request=request
    )

    assert queryset.count() == 3


@pytest.mark.django_db
def test_agenda_item_admin_save_model(hour, agenda_item_admin, request_builder):
    RoomFactory()
    RoomFactory()
    proposal = ProposalFactory(
        duration_minutes=2, meeting=MeetingFactory(publication_time=hour(-1))
    )
    room = RoomFactory()
    request = request_builder(room_id=room.id)
    agenda_item = AgendaItemFactory(meeting=proposal.meeting)

    agenda_item_admin.save_model(
        request=request, obj=agenda_item, form=Mock(), change=True
    )

    meeting = Meeting.objects.get(id=agenda_item.meeting.id)
    assert meeting.start_time == hour(2)
    assert meeting.end_time == hour(3)
    assert meeting.location == agenda_item.room.name


@pytest.mark.django_db
def test_agenda_item_admin_delete(hour, agenda_item_admin, request_builder):
    RoomFactory()
    RoomFactory()
    proposal = ProposalFactory(
        duration_minutes=2, meeting=MeetingFactory(publication_time=hour(-1))
    )
    agenda_item = AgendaItemFactory(meeting=proposal.meeting)
    meeting_id = agenda_item.meeting.id
    room = RoomFactory()
    request = request_builder(room_id=room.id)

    agenda_item_admin.delete_model(request=request, obj=agenda_item)

    meeting = Meeting.objects.get(id=meeting_id)
    assert meeting.start_time is None
    assert meeting.end_time is None
    assert meeting.location == ""

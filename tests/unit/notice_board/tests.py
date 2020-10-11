from datetime import timedelta
from unittest.mock import Mock

import pytest
from django.contrib import admin
from django.utils import timezone
from rest_framework.serializers import ValidationError

from chronology.models import AgendaItem
from notice_board.admin import SphereManagersAdminMixin
from notice_board.apps import NoticeBoardConfig
from notice_board.models import DescribedModel, Guild, Sphere
from notice_board.serializers import (
    MeetingCreateSerializer,
    MeetingReadSerializer,
    MeetingUpdateSerializer,
)
from notice_board.viewsets import MeetingViewSet
from tests.factories import GuildFactory, MeetingFactory, SphereFactory, UserFactory


class SphereManagersAdmin(SphereManagersAdminMixin, admin.ModelAdmin):
    pass


@pytest.mark.parametrize(
    "model, return_value, is_superuser",
    [
        (
            "AgendaItem",
            Mock(filter=lambda room__festival__sphere__managers: [1, 2, 3]),
            False,
        ),
        ("Festival", Mock(filter=lambda sphere__managers: [1, 2, 3]), False),
        ("Helper", Mock(filter=lambda festival__sphere__managers: [1, 2, 3]), False),
        ("Meeting", Mock(filter=lambda sphere__managers: [1, 2, 3]), False),
        (
            "Proposal",
            Mock(filter=lambda waitlist__festival__sphere__managers: [1, 2, 3]),
            False,
        ),
        ("Room", Mock(filter=lambda festival__sphere__managers: [1, 2, 3]), False),
        ("Site", Mock(filter=lambda sphere__managers: [1, 2, 3]), False),
        ("Sphere", Mock(filter=lambda managers: [1, 2, 3]), False),
        ("TimeSlot", Mock(filter=lambda festival__sphere__managers: [1, 2, 3]), False),
        ("WaitList", Mock(filter=lambda festival__sphere__managers: [1, 2, 3]), False),
        ("User", [1, 2, 3], False),
        ("Guild", [1, 2, 3], False),
        ("Meeting", [1, 2, 3], True),
    ],
)
def test_get_queryset(model, return_value, is_superuser):
    model = Mock(__name__=model)
    model_admin = SphereManagersAdmin(model=model, admin_site=Mock())
    model_admin.model._default_manager.get_queryset = Mock(return_value=return_value)
    request = Mock()
    request.user.is_superuser = is_superuser

    queryset = model_admin.get_queryset(request)

    assert queryset == [1, 2, 3]


def test_get_list_display():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=Mock())

    assert model_admin.get_list_display(Mock()) == ["id", "__str__"]


def test_get_list_display_links():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=Mock())

    assert model_admin.get_list_display_links(Mock(), ["id", "__str__"]) == [
        "id",
        "__str__",
    ]


def test_get_list_display_links_field_is_on_list():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=Mock())
    model_admin.list_display_links = ["id", "__str__"]

    assert model_admin.get_list_display_links(Mock(), ["id", "__str__"]) == [
        "id",
        "__str__",
    ]


def test_notice_board_config():
    assert NoticeBoardConfig.name == "notice_board"


@pytest.mark.parametrize(
    "model, name", ((DescribedModel, "dmodel"), (Sphere, "sphere"))
)
def test_str(model, name):
    assert str(model(name=name)) == name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, slug",
    (
        ("dmodel", "dmodel"),
        ("Brotherhood of steel", "brotherhood-of-steel"),
        ("x" * 100, "x" * 48),
    ),
)
def test_unique_slug(name, slug):
    model = Guild(name=name)

    model.save()

    assert model.slug == slug


@pytest.mark.django_db
def test_duplicate_meeting_names_in_different_spheres():
    name = "Silkworm Breeders Annual Conference"

    meeting_1 = MeetingFactory(name=name)
    meeting_2 = MeetingFactory(name=name)
    meeting_3 = MeetingFactory(name=name)

    assert meeting_1.slug == "silkworm-breeders-annual-conference"
    assert meeting_2.slug == "silkworm-breeders-annual-conference"
    assert meeting_3.slug == "silkworm-breeders-annual-conference"


@pytest.mark.django_db
def test_unique_meeting_slugs():
    name = "Silkworm Breeders Annual Conference"
    sphere = SphereFactory()

    meeting_1 = MeetingFactory(name=name, sphere=sphere)
    meeting_2 = MeetingFactory(name=name, sphere=sphere)
    meeting_3 = MeetingFactory(name=name, sphere=sphere)

    assert meeting_1.slug == "silkworm-breeders-annual-conference"
    assert meeting_2.slug == "silkworm-breeders-annual-conference-1"
    assert meeting_3.slug == "silkworm-breeders-annual-conference-2"


def _set_filter_queryset(remote_model):
    remote_model.objects.all.return_value = []
    remote_model._default_manager.using().order_by().filter.return_value = [1, 2, 3]


def _set_empty_queryset(remote_model):
    remote_model.objects.all().filter.return_value = [1, 2, 3]
    remote_model._default_manager.using().order_by.return_value = None


def _set_empty_request_queryset(remote_model):
    remote_model.objects.all.return_value = [1, 2, 3]
    remote_model._default_manager.using().order_by.return_value = None


@pytest.mark.parametrize(
    "set_remote_model_mock,empty_request",
    (
        (_set_filter_queryset, False),
        (_set_empty_queryset, False),
        (_set_empty_request_queryset, True),
    ),
)
def test_get_field_queryset(set_remote_model_mock, empty_request):
    admin_site = Mock()
    related_admin = Mock()
    related_admin.get_ordering.return_value = []
    admin_site._registry.get.return_value = related_admin
    model = Mock(__name__="Meeting")
    model_admin = SphereManagersAdmin(model=model, admin_site=admin_site)
    db_field = Mock()
    remote_model = db_field.remote_field.model
    remote_model.__name__ = "Sphere"
    set_remote_model_mock(remote_model)
    request = Mock()
    request.user.is_superuser = False
    if empty_request:
        request = None

    queryset = model_admin.get_field_queryset(
        db=None, db_field=db_field, request=request
    )

    assert queryset == [1, 2, 3]


@pytest.mark.parametrize(
    "method,model,expected",
    (
        ("has_add_permission", AgendaItem, False),
        ("has_change_permission", AgendaItem, False),
        ("has_delete_permission", AgendaItem, False),
        ("has_add_permission", Mock(), True),
        ("has_change_permission", Mock(), True),
        ("has_delete_permission", Mock(), True),
    ),
)
def test_popup_permissions(method, model, expected):
    request = Mock()
    if not isinstance(model, AgendaItem):
        request.resolver_match = Mock(url_name="chronology_agendaitem_add")

    sphere_managers_admin = SphereManagersAdmin(model=model, admin_site=Mock())

    assert (getattr(sphere_managers_admin, method)(request) is False) is expected


@pytest.mark.parametrize(
    "action,serializer",
    (
        ("create", MeetingCreateSerializer),
        ("read", MeetingReadSerializer),
        ("custom_action", MeetingReadSerializer),
        ("destroy", MeetingReadSerializer),
        ("list", MeetingReadSerializer),
        ("update", MeetingUpdateSerializer),
    ),
)
def test_meeting_viewset_get_serializer_class(action, serializer):
    viewset = MeetingViewSet()
    viewset.action = action

    serializer_class = viewset.get_serializer_class()

    assert serializer_class == serializer


@pytest.mark.django_db
def test_meeting_create_serializer_validate_guild_none():
    serializer = MeetingCreateSerializer()

    assert serializer.validate_guild(None) is None


@pytest.mark.django_db
def test_meeting_create_serializer_validate_guild_error():
    guild = GuildFactory()
    serializer = MeetingCreateSerializer(context={"request": Mock(user=UserFactory())})

    with pytest.raises(ValidationError) as exc_info:
        serializer.validate_guild(guild)

    assert (
        str(exc_info.value.detail[0])
        == "You cannot add meeting to a guild you don't belong!"
    )


@pytest.mark.django_db
def test_meeting_create_serializer_validate_guild():
    user = UserFactory()
    guild = GuildFactory()
    guild.members.add(user)
    serializer = MeetingCreateSerializer(context={"request": Mock(user=user)})

    result = serializer.validate_guild(guild)

    assert result == guild


@pytest.mark.django_db
def test_meeting_create_serializer_validate_organizer_error():
    organizer = UserFactory()
    serializer = MeetingCreateSerializer(context={"request": Mock(user=UserFactory())})

    with pytest.raises(ValidationError) as exc_info:
        serializer.validate_organizer(organizer)

    assert (
        str(exc_info.value.detail[0]) == "You cannot add meeting as a different person!"
    )


@pytest.mark.django_db
def test_meeting_create_serializer_validate_organizer():
    user = UserFactory()
    serializer = MeetingCreateSerializer(context={"request": Mock(user=user)})

    result = serializer.validate_organizer(user)

    assert result == user


@pytest.mark.django_db
def test_meeting_create_serializer_validate_start_time_error():
    start_time = timezone.localtime(timezone.now()) - timedelta(days=1)
    serializer = MeetingCreateSerializer()

    with pytest.raises(ValidationError) as exc_info:
        serializer.validate_start_time(start_time)

    assert str(exc_info.value.detail[0]) == "You cannot add a meeting in the past!"


@pytest.mark.django_db
def test_meeting_create_serializer_validate_start_time():
    start_time = timezone.localtime(timezone.now()) + timedelta(days=1)
    serializer = MeetingCreateSerializer()

    result = serializer.validate_start_time(start_time)

    assert result == start_time

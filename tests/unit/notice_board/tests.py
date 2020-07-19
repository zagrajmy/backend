# pylint: disable=protected-access
from unittest.mock import Mock

import pytest
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from notice_board.admin import SphereManagersAdminMixin
from notice_board.apps import NoticeBoardConfig
from notice_board.models import DescribedModel, Sphere


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
    model_admin = SphereManagersAdmin(model=model, admin_site=AdminSite())
    model_admin.model._default_manager.get_queryset = Mock(return_value=return_value)
    request = Mock()
    request.user.is_superuser = is_superuser

    queryset = model_admin.get_queryset(request)

    assert queryset == [1, 2, 3]


def test_get_list_display():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=AdminSite())

    assert model_admin.get_list_display(Mock()) == ["id", "__str__"]


def test_get_list_display_links():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=AdminSite())

    assert model_admin.get_list_display_links(Mock(), ["id", "__str__"]) == [
        "id",
        "__str__",
    ]


def test_get_list_display_links_field_is_on_list():
    model_admin = SphereManagersAdmin(model=Mock(), admin_site=AdminSite())
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


def _prepare_admin():
    model = Mock(__name__="Meeting")
    admin_site = Mock()
    related_admin = Mock()
    related_admin.get_ordering.return_value = []
    admin_site._registry.get.return_value = related_admin
    model_admin = SphereManagersAdmin(model=model, admin_site=admin_site)
    db_field = Mock()
    remote_model = db_field.remote_field.model
    remote_model.__name__ = "Sphere"
    return model_admin, db_field, remote_model


def test_get_field_queryset():
    model_admin, db_field, remote_model = _prepare_admin()

    remote_model.objects.all.return_value = []
    remote_model._default_manager.using().order_by().filter.return_value = [1, 2, 3]
    request = Mock()
    request.user.is_superuser = False
    queryset = model_admin.get_field_queryset(
        db=None, db_field=db_field, request=request
    )

    assert queryset == [1, 2, 3]


def test_get_field_queryset_empty_queryset():
    model_admin, db_field, remote_model = _prepare_admin()

    remote_model.objects.all().filter.return_value = [1, 2, 3]
    remote_model._default_manager.using().order_by.return_value = None
    request = Mock()
    request.user.is_superuser = False
    queryset = model_admin.get_field_queryset(
        db=None, db_field=db_field, request=request
    )

    assert queryset == [1, 2, 3]


def test_get_field_queryset_no_request():
    model_admin, db_field, remote_model = _prepare_admin()

    remote_model.objects.all.return_value = [1, 2, 3]
    remote_model._default_manager.using().order_by.return_value = None
    queryset = model_admin.get_field_queryset(db=None, db_field=db_field, request=None)

    assert queryset == [1, 2, 3]

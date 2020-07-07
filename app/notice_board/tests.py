from unittest.mock import Mock

import pytest

from notice_board.admin import SphereManagersAdmin


@pytest.mark.parametrize(
    "model, return_value",
    [
        ("AgendaItem", Mock(filter=lambda room__festival__sphere__managers: [1, 2, 3])),
        ("Festival", Mock(filter=lambda sphere__managers: [1, 2, 3])),
        ("Helper", Mock(filter=lambda festival__sphere__managers: [1, 2, 3])),
        ("Meeting", Mock(filter=lambda sphere__managers: [1, 2, 3])),
        (
            "Proposal",
            Mock(filter=lambda waitlist__festival__sphere__managers: [1, 2, 3]),
        ),
        ("Room", Mock(filter=lambda festival__sphere__managers: [1, 2, 3])),
        ("Site", Mock(filter=lambda sphere__managers: [1, 2, 3])),
        ("Sphere", Mock(filter=lambda managers: [1, 2, 3])),
        ("TimeSlot", Mock(filter=lambda festival__sphere__managers: [1, 2, 3])),
        ("WaitList", Mock(filter=lambda festival__sphere__managers: [1, 2, 3])),
    ],
)
def test_get_queryset(model, return_value):
    model = Mock(__name__=model)
    admin = SphereManagersAdmin(model=model, admin_site=Mock())
    # pylint: disable=protected-access
    admin.model._default_manager.get_queryset = Mock(return_value=return_value)
    request = Mock()
    request.user.is_superuser = False

    queryset = admin.get_queryset(request)

    assert queryset == [1, 2, 3]


def test_get_list_display():
    admin = SphereManagersAdmin(model=Mock(), admin_site=Mock())

    assert admin.get_list_display(Mock()) == ["id", "__str__"]


def test_get_list_display_links():
    admin = SphereManagersAdmin(model=Mock(), admin_site=Mock())

    assert admin.get_list_display_links(Mock(), ["id", "__str__"]) == ["__str__"]


def test_get_queryset_superuser():
    model = Mock(__name__="MyModel")
    admin = SphereManagersAdmin(model=model, admin_site=Mock())
    # pylint: disable=protected-access
    admin.model._default_manager.get_queryset = Mock(return_value=[1, 2, 3])
    request = Mock()
    request.user.is_superuser = True

    queryset = admin.get_queryset(request)

    assert queryset == [1, 2, 3]


def test_get_queryset_no_filter():
    model = Mock(__name__="User")
    admin = SphereManagersAdmin(model=model, admin_site=Mock())
    # pylint: disable=protected-access
    admin.model._default_manager.get_queryset = Mock(return_value=[1, 2, 3])
    request = Mock()
    request.user.is_superuser = False

    queryset = admin.get_queryset(request)

    assert queryset == [1, 2, 3]

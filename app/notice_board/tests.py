from unittest.mock import Mock

import pytest

from notice_board.admin import SphereManagersAdmin


@pytest.mark.parametrize(
    "admin_class,return_value,is_superuser",
    [
        (SphereManagersAdmin, [1, 2, 3], True),
        (SphereManagersAdmin, Mock(filter=lambda managers: [1, 2, 3]), False),
        (SphereManagersAdmin, Mock(filter=lambda sphere__managers: [1, 2, 3]), False),
        (SphereManagersAdmin, Mock(filter=lambda sphere__managers: [1, 2, 3]), False),
    ],
)
def test_get_queryset(admin_class, return_value, is_superuser):
    admin = admin_class(model=Mock(), admin_site=Mock())
    # pylint: disable=protected-access
    admin.model._default_manager.get_queryset = Mock(return_value=return_value)
    request = Mock()
    request.user.is_superuser = is_superuser

    queryset = admin.get_queryset(request)

    assert queryset == [1, 2, 3]

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from trekking_and_tour_management_system.users.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.pk}/"

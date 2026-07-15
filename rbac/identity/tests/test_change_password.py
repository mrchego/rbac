import pytest
from rbac.accounts.models import User
from rbac.identity.services import change_password
from rbac.core.exceptions import AppValidationError


@pytest.mark.django_db
class TestChangePassword:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@example.com",
            password="oldpassword",
        )

    def test_change_password_success(self, user):
        new_password = "NewSecurePass123"
        change_password(user, new_password)
        user.refresh_from_db()
        assert user.check_password(new_password) is True
        assert user.last_password_change is not None
        assert user.failed_login_attempts == 0
        assert user.locked_until is None
        assert user.password_reset_required is False

    def test_change_password_weak(self, user):
        with pytest.raises(AppValidationError) as exc:
            change_password(user, "123")
        assert "Password must be at least 8 characters long" in str(exc.value)
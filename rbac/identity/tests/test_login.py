import pytest
from django.utils import timezone
from rbac.accounts.models import User
from rbac.accounts.selectors import get_user_by_email
from rbac.identity.services import login, handle_failed_login, handle_successful_login
from rbac.core.exceptions import ApplicationError, ErrorCode
from rbac.identity.constants import MAX_FAILED_ATTEMPTS, LOCKOUT_DURATION_MINUTES


@pytest.mark.django_db
class TestLoginService:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            can_login=True,
            is_active=True,
        )

    def test_valid_login(self, user):
        logged_in_user = login(email="test@example.com", password="password123")
        assert logged_in_user == user
        assert logged_in_user.failed_login_attempts == 0
        assert logged_in_user.locked_until is None
        assert logged_in_user.last_login is not None

    def test_wrong_password(self, user):
        with pytest.raises(ApplicationError) as exc:
            login(email="test@example.com", password="wrong")
        assert exc.value.code == ErrorCode.INVALID_CREDENTIALS
        user.refresh_from_db()
        assert user.failed_login_attempts == 1
        assert user.locked_until is None

    def test_unknown_email(self):
        with pytest.raises(ApplicationError) as exc:
            login(email="unknown@example.com", password="anything")
        assert exc.value.code == ErrorCode.INVALID_CREDENTIALS

    def test_locked_account(self, user):
        user.locked_until = timezone.now() + timezone.timedelta(minutes=10)
        user.save()
        with pytest.raises(ApplicationError) as exc:
            login(email="test@example.com", password="password123")
        assert exc.value.code == ErrorCode.ACCOUNT_LOCKED

    def test_inactive_account(self, user):
        user.is_active = False
        user.save()
        with pytest.raises(ApplicationError) as exc:
            login(email="test@example.com", password="password123")
        assert exc.value.code == ErrorCode.ACCOUNT_INACTIVE

    def test_account_disabled(self, user):
        user.can_login = False
        user.save()
        with pytest.raises(ApplicationError) as exc:
            login(email="test@example.com", password="password123")
        assert exc.value.code == ErrorCode.ACCOUNT_DISABLED

    def test_failed_attempts_increment(self, user):
        for _ in range(MAX_FAILED_ATTEMPTS - 1):
            with pytest.raises(ApplicationError):
                login(email="test@example.com", password="wrong")
            user.refresh_from_db()
            assert user.failed_login_attempts == _ + 1

        # Last attempt should lock
        with pytest.raises(ApplicationError):
            login(email="test@example.com", password="wrong")
        user.refresh_from_db()
        assert user.failed_login_attempts == MAX_FAILED_ATTEMPTS
        assert user.locked_until is not None
        assert user.locked_until > timezone.now()

    def test_successful_login_resets_counter(self, user):
        # Simulate 3 failed attempts
        for _ in range(3):
            with pytest.raises(ApplicationError):
                login(email="test@example.com", password="wrong")
        user.refresh_from_db()
        assert user.failed_login_attempts == 3

        # Now successful login
        login(email="test@example.com", password="password123")
        user.refresh_from_db()
        assert user.failed_login_attempts == 0
        assert user.locked_until is None
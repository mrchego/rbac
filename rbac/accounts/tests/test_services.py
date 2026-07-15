import pytest
from django.utils import timezone

from rbac.accounts.models import User
from rbac.accounts.services import (
    create_user,
    update_user,
    change_password,
    activate_user,
    deactivate_user,  # You have this, not disable_user
    lock_user,
    unlock_user,
    force_password_reset,
)
from rbac.core.exceptions import AppValidationError, BusinessRuleViolationError, ApplicationError
from rbac.company.models import Company


@pytest.mark.django_db
class TestAccountServices:

    @pytest.fixture
    def company(self):
        return Company.objects.create(
            name="Test Company",
            email="test@company.com",
            phone="+1234567890",
            country="USA",
            city="New York",
            address="123 Test St",
        )

    @pytest.fixture
    def user_data(self):
        return {
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "SecurePass123",
            "phone": "+1234567890",
            "can_login": True,
            "is_active": True,
        }

    @pytest.fixture
    def existing_user(self, company):
        user = User.objects.create_user(
            email="existing@example.com",
            password="OldPass123",
            first_name="Existing",
            last_name="User",
            company=company,
        )
        user.last_password_change = timezone.now() - timezone.timedelta(days=30)
        user.save()
        return user

    # --- Test create_user ---
    def test_create_user_success(self, user_data, company):
        user = create_user(**user_data, company=company)
        assert user.email == "john.doe@example.com"
        assert user.check_password("SecurePass123") is True

    def test_create_user_weak_password_raises_validation_error(self, user_data, company):
        user_data["password"] = "123"
        with pytest.raises(AppValidationError) as exc:
            create_user(**user_data, company=company)
        assert "Password must be at least 8 characters long" in str(exc.value)

    def test_create_user_duplicate_email_raises_business_rule_error(self, user_data, company, existing_user):
        user_data["email"] = existing_user.email
        with pytest.raises(BusinessRuleViolationError) as exc:
            create_user(**user_data, company=company)
        assert "A user with this email already exists" in str(exc.value)

    # --- Test update_user ---
    def test_update_user_success(self, existing_user):
        updated_user = update_user(
            user_id=existing_user.id,
            first_name="Updated",
            last_name="Name",
            phone="+1987654321",
        )
        assert updated_user.first_name == "Updated"
        assert updated_user.phone == "+1987654321"

    def test_update_user_not_found_raises_application_error(self):
        with pytest.raises(ApplicationError) as exc:
            update_user(user_id="00000000-0000-0000-0000-000000000000", first_name="Ghost")
        assert "User not found" in str(exc.value)

    # --- Test change_password ---
    def test_change_password_success(self, existing_user):
        new_password = "NewSecurePass456"
        old_timestamp = existing_user.last_password_change
        existing_user.failed_login_attempts = 5
        existing_user.save()

        change_password(existing_user, new_password)
        existing_user.refresh_from_db()
        
        assert existing_user.check_password(new_password) is True
        assert existing_user.last_password_change > old_timestamp
        assert existing_user.failed_login_attempts == 0  # Resets locks

    def test_change_password_weak_password_raises_validation_error(self, existing_user):
        with pytest.raises(AppValidationError) as exc:
            change_password(existing_user, "123")
        assert "Password must be at least 8 characters long" in str(exc.value)

    # --- Test activate/deactivate ---
    def test_activate_user(self, existing_user):
        existing_user.is_active = False
        existing_user.save()
        
        activated_user = activate_user(user_id=existing_user.id)
        assert activated_user.is_active is True

    def test_deactivate_user(self, existing_user):
        # Testing your actual deactivate_user function
        assert existing_user.is_active is True
        deactivated_user = deactivate_user(user_id=existing_user.id)
        
        assert deactivated_user.is_active is False
        # deactivate_user should *only* toggle is_active, not can_login!
        assert deactivated_user.can_login is True

    # --- Test lock/unlock ---
    def test_lock_user(self, existing_user):
        locked_user = lock_user(user_id=existing_user.id, duration_minutes=15)
        assert locked_user.locked_until is not None
        assert locked_user.locked_until > timezone.now()

    def test_unlock_user(self, existing_user):
        existing_user.locked_until = timezone.now() + timezone.timedelta(minutes=15)
        existing_user.failed_login_attempts = 5
        existing_user.save()
        
        unlocked_user = unlock_user(user_id=existing_user.id)
        assert unlocked_user.locked_until is None
        assert unlocked_user.failed_login_attempts == 0

    # --- Test force_password_reset ---
    def test_force_password_reset(self, existing_user):
        user = force_password_reset(user_id=existing_user.id)
        assert user.password_reset_required is True
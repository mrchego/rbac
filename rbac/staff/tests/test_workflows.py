import pytest
import uuid
from django.utils import timezone
from rbac.accounts.models import User
from rbac.company.models import Company
from rbac.staff.models import Invitation
from rbac.staff.workflows import invite_staff, accept_invitation
from rbac.core.exceptions import ApplicationError, ErrorCode


@pytest.mark.django_db
class TestStaffWorkflows:

    # --------------------------
    # Fixtures
    # --------------------------
    @pytest.fixture
    def company(self):
        return Company.objects.create(
            name="Test Company",
            email="company@test.com",
            phone="+1234567890",
            country="US",
            city="NY",
            address="123 Test St",
            is_active=True,
        )

    @pytest.fixture
    def invited_by(self, company):
        return User.objects.create_user(
            email="admin@test.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            company=company,
            is_staff=True,
        )

    @pytest.fixture
    def request_factory(self):
        from django.test import RequestFactory
        return RequestFactory()

    # --------------------------
    # Tests
    # --------------------------
    def test_invite_staff_success(self, company, invited_by, request_factory):
        request = request_factory.post('/')
        
        user, invitation = invite_staff(
            email="staff@test.com",
            first_name="Staff",
            last_name="Member",
            company=company,
            invited_by=invited_by,
            request=request,
        )

        # Check user created correctly (inactive, no login, unusable password)
        assert user.email == "staff@test.com"
        assert user.company == company
        assert user.is_active is False
        assert user.can_login is False
        assert user.has_usable_password() is False

        # Check invitation created correctly
        assert invitation.email == "staff@test.com"
        assert invitation.company == company
        assert invitation.invited_by == invited_by
        assert invitation.used is False
        assert invitation.token is not None

    def test_invite_staff_duplicate_email(self, company, invited_by, request_factory):
        request = request_factory.post('/')
        
        # Create an active user with this email first
        User.objects.create_user(
            email="existing@test.com",
            password="pass123",
            company=company,
            is_active=True,
        )

        with pytest.raises(ApplicationError) as exc:
            invite_staff(
                email="existing@test.com",
                first_name="Duplicate",
                last_name="User",
                company=company,
                invited_by=invited_by,
                request=request,
            )
        assert exc.value.code == ErrorCode.USER_ALREADY_EXISTS

    def test_accept_invitation_success(self, company, invited_by, request_factory):
        request = request_factory.post('/')
        
        # 1. Invite the staff member
        user, invitation = invite_staff(
            email="staff2@test.com",
            first_name="Accept",
            last_name="Test",
            company=company,
            invited_by=invited_by,
            request=request,
        )
        
        # 2. Accept the invitation
        new_password = "SecurePass123"
        activated_user = accept_invitation(
            token=invitation.token,
            new_password=new_password,
        )

        # Check user is activated
        activated_user.refresh_from_db()
        assert activated_user.is_active is True
        assert activated_user.can_login is True
        assert activated_user.check_password(new_password) is True

        # Check invitation is marked as used
        invitation.refresh_from_db()
        assert invitation.used is True
        assert invitation.accepted_at is not None

    def test_accept_invitation_invalid_token(self):
        invalid_token = uuid.uuid4()
        with pytest.raises(ApplicationError) as exc:
            accept_invitation(
                token=invalid_token,
                new_password="SecurePass123",
            )
        assert exc.value.code == ErrorCode.INVALID_TOKEN
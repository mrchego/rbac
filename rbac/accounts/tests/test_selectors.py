import pytest
from rbac.accounts.models import User
from rbac.accounts.selectors import get_user, get_user_by_email, list_users
from rbac.company.models import Company

@pytest.mark.django_db
class TestAccountSelectors:

    # -------------------------------------------------------------
    # Fixtures (copied from test_services.py)
    # -------------------------------------------------------------
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
    def existing_user(self, company):
        user = User.objects.create_user(
            email="existing@example.com",
            password="OldPass123",
            first_name="Existing",
            last_name="User",
            company=company,
        )
        return user

    # -------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------
    def test_get_user_found(self, existing_user):
        user = get_user(user_id=existing_user.id)
        assert user == existing_user

    def test_get_user_not_found(self):
        user = get_user(user_id="00000000-0000-0000-0000-000000000000")
        assert user is None  # Selectors must return None, not raise!

    def test_get_user_by_email_found(self, existing_user):
        user = get_user_by_email(email=existing_user.email)
        assert user == existing_user

    def test_get_user_by_email_not_found(self):
        user = get_user_by_email(email="missing@example.com")
        assert user is None

    def test_list_users_filter_by_company(self, company, existing_user):
        users = list_users(company_id=company.id)
        assert existing_user in users
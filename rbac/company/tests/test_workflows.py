import pytest
from rbac.company.workflows import register_company
from rbac.accounts.models import User
from rbac.company.models import Company

@pytest.mark.django_db
class TestRegisterCompany:
    def test_register_company_success(self, rf):
        request = rf.post('/')  # dummy request for email generation
        company, admin = register_company(
            company_name="Test Co",
            company_email="company@test.com",
            company_phone="+1234567890",
            company_country="US",
            company_city="NY",
            company_address="123 Street",
            admin_email="admin@test.com",
            admin_password="SecurePass123",
            admin_first_name="John",
            admin_last_name="Doe",
            request=request,
        )
        assert Company.objects.count() == 1
        assert User.objects.count() == 1
        assert admin.company == company
        assert admin.is_staff is True
        # Email verification should be sent (we can mock the send function later)
from django.db import transaction, IntegrityError
from rbac.company.models import Company, CompanySettings
from rbac.company.validators import validate_company_name
from rbac.core.exceptions import BusinessRuleViolationError, ErrorCode
from rbac.core.validators.phone import validate_phone_number


@transaction.atomic
def create_company(*, name, email, phone, country, city, address, logo_light=None, logo_dark=None):
    if Company.objects.exists():
        raise BusinessRuleViolationError("There can only be one company.", code=ErrorCode.COMPANY_ALREADY_EXISTS)

    # Validators raise AppValidationError directly. No try/except needed here anymore!
    validate_company_name(name)
    validate_phone_number(phone)

    try:
        company = Company.objects.create(
            name=name, logo_light=logo_light, logo_dark=logo_dark,
            email=email, phone=phone, country=country, city=city, address=address,
            is_active=True
        )
        CompanySettings.objects.create(company=company)
        return company
    except IntegrityError:
        raise BusinessRuleViolationError("A company with this email already exists.", code=ErrorCode.COMPANY_ALREADY_EXISTS)
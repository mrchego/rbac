from rbac.company.models import CompanySettings
from rbac.core.exceptions import ApplicationError, ErrorCode


def get_company_settings(*, company):
    settings = CompanySettings.objects.filter(company=company).first()

    if not settings:
        raise ApplicationError(
            "Company settings not found.",
            code=ErrorCode.COMPANY_NOT_FOUND,
        )

    return settings
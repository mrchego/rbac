from rbac.company.models import Company
from rbac.core.exceptions import ApplicationError, ErrorCode


def get_company():
    company = Company.objects.first()

    if not company:
        raise ApplicationError(
            "No company has been registered yet.",
            code=ErrorCode.COMPANY_NOT_FOUND,
        )

    return company
import strawberry
from rbac.company.graphql.types import CompanyType, CompanySettingsType
from rbac.company.selectors import get_company, get_company_settings


@strawberry.type
class CompanyQuery:
    @strawberry.field
    def company(self, info: strawberry.Info) -> CompanyType:
        return get_company()

    @strawberry.field
    def company_settings(self, info: strawberry.Info) -> CompanySettingsType:
        company = get_company()
        return get_company_settings(company=company)
import strawberry
from rbac.company.graphql.inputs import (
    CreateCompanyInput,
    RegisterCompanyInput,
    UpdateCompanyInput,
    UpdateCompanySettingsInput,
)
from rbac.company.graphql.payloads import CompanyMutationPayload, CompanySettingsMutationPayload
from rbac.company.selectors import get_company
from rbac.company.services import update_company as update_action
from rbac.company.services import update_company_settings as update_settings_action
from rbac.company.workflows import register_company as register_company_workflow
from rbac.authorization.decorators import require_owner
from rbac.core.exceptions import ApplicationError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class CompanyMutation:
    @strawberry.mutation
    def register_company(self, info: strawberry.Info, input: RegisterCompanyInput) -> CompanyMutationPayload:
        # No auth check — this is the bootstrap step, before any user exists.
        # create_company already refuses if a company has already been registered.
        try:
            company, admin = register_company_workflow(
                company_name=input.name,
                company_email=input.email,
                company_phone=input.phone,
                company_country=input.country,
                company_city=input.city,
                company_address=input.address,
                company_logo_light=input.logo_light,
                company_logo_dark=input.logo_dark,
                admin_email=input.admin_email,
                admin_password=input.admin_password,
                admin_first_name=input.admin_first_name,
                admin_last_name=input.admin_last_name,
                request=info.context.request,
            )
            return CompanyMutationPayload(success=True, company=company)
        except ApplicationError as e:
            return CompanyMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_owner()
    def update_company(self, info: strawberry.Info, input: UpdateCompanyInput) -> CompanyMutationPayload:
        try:
            current_company = get_company()
            company = update_action(
                company_id=current_company.id,
                name=input.name,
                logo_light=input.logo_light,
                logo_dark=input.logo_dark,
                email=input.email,
                phone=input.phone,
                country=input.country,
                city=input.city,
                address=input.address,
                is_active=input.is_active,
            )
            return CompanyMutationPayload(success=True, company=company)
        except ApplicationError as e:
            return CompanyMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_owner()
    def update_company_settings(self, info: strawberry.Info, input: UpdateCompanySettingsInput) -> CompanySettingsMutationPayload:
        try:
            company = get_company()
            settings = update_settings_action(
                company=company,
                timezone=input.timezone,
                currency=input.currency,
                language=input.language,
                date_format=input.date_format,
                theme=input.theme,
            )
            return CompanySettingsMutationPayload(success=True, settings=settings)
        except ApplicationError as e:
            return CompanySettingsMutationPayload(success=False, errors=[format_application_error(e)])
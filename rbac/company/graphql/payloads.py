import strawberry
from typing import Optional, List

from rbac.company.graphql.types import CompanyType, CompanySettingsType
from rbac.core.graphql.errors import MutationError


@strawberry.type
class CompanyMutationPayload:
    success: bool
    company: Optional[CompanyType] = None
    errors: Optional[List[MutationError]] = None


@strawberry.type
class CompanySettingsMutationPayload:
    success: bool
    settings: Optional[CompanySettingsType] = None
    errors: Optional[List[MutationError]] = None
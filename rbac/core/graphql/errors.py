import strawberry
from typing import Optional
from rbac.core.exceptions import ApplicationError

@strawberry.type
class MutationError:
    message: str
    code: str
    field: Optional[str] = None

def format_application_error(error: ApplicationError) -> MutationError:
    return MutationError(
        message=error.message,
        code=getattr(error, 'code', 'APPLICATION_ERROR'),
        field=getattr(error, 'field', None)
    )
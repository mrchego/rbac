class ApplicationError(Exception):
    def __init__(self, message: str, code: str = None, field: str = None):
        self.message = message
        self.code = code or "APPLICATION_ERROR"
        self.field = field
        super().__init__(message)


class AppValidationError(ApplicationError):
    def __init__(self, message, field=None):
        super().__init__(message, code="VALIDATION_ERROR", field=field)


class AppPermissionDeniedError(ApplicationError):
    def __init__(self, message="You do not have permission to perform this action."):
        super().__init__(message, code="PERMISSION_DENIED")


class BusinessRuleViolationError(ApplicationError):
    def __init__(self, message, code=None):
        super().__init__(message, code=code or "BUSINESS_RULE_VIOLATION")


class ErrorCode:
    # General
    VALIDATION_ERROR = "VALIDATION_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    BUSINESS_RULE = "BUSINESS_RULE"
    
    # Authentication
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"
    INVALID_TOKEN = "INVALID_TOKEN"

    # Domain-specific
    COMPANY_NOT_FOUND = "COMPANY_NOT_FOUND"
    COMPANY_ALREADY_EXISTS = "COMPANY_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    ROLE_NOT_FOUND = "ROLE_NOT_FOUND"

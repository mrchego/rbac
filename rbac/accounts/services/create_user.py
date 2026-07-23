from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from rbac.accounts.models import User
from rbac.accounts.validators import validate_password_strength
from rbac.core.exceptions import AppValidationError, BusinessRuleViolationError, ErrorCode
from rbac.core.validators.email import validate_email
from rbac.core.validators.phone import validate_phone_number

@transaction.atomic
def create_user(*, email, first_name, last_name, password=None, phone=None, avatar=None, company=None,
                can_login=True, is_active=True, is_staff=False, is_superuser=False, is_founder=False):
    validate_email(email)
    if phone:
        validate_phone_number(phone)

    if password is not None:
        try:
            validate_password_strength(password)
        except ValidationError as e:
            raise AppValidationError(e.message, field="password")

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone or "",
        avatar=avatar,
        company=company,
        can_login=can_login,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_founder=is_founder,
    )
    
    # If password is provided, hash it. Otherwise, set an unusable password.
    if password is not None:
        user.set_password(password)
    else:
        user.set_unusable_password()

    # Validation happens before hitting the DB – catches duplicate email via full_clean
    try:
        user.full_clean()
        user.save()
        return user
    except ValidationError as e:
        if 'email' in e.message_dict:
            raise BusinessRuleViolationError(
                "A user with this email already exists.",
                code=ErrorCode.USER_ALREADY_EXISTS,
            )
        raise AppValidationError(e.messages[0], field=list(e.message_dict.keys())[0])
    except IntegrityError:
        # Fallback – rare race condition; treat as duplicate email
        raise BusinessRuleViolationError(
            "A user with this email already exists.",
            code=ErrorCode.USER_ALREADY_EXISTS,
        )
def get_current_user(info):
    """Extracts the authenticated user from the GraphQL context."""
    request = info.context.request
    if not request.user.is_authenticated:
        return None
    return request.user
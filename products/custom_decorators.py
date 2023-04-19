from django.contrib.admin.views.decorators import user_passes_test


def superuser_required(view_func=None, home='/',):
    """
    Custom decorator for checking both superuser and active status and
    redirecting to home page if not.
    """
    superuser_check = user_passes_test(
        lambda u: u.is_superuser and u.is_active,
        login_url=home,
        redirect_field_name='',
    )
    if view_func:
        return superuser_check(view_func)
    return superuser_check

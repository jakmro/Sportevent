from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class EmailVerificationRequiredMixin(AccessMixin):
    """Mixin that verifies it user's email is verified."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.email_verified:
            return redirect('email_verification')
        return super().dispatch(request, *args, **kwargs)

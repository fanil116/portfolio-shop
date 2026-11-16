from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request


class EnforceCsrfMixin:
    """Проверяет CSRF для перечисленных действий даже у анонимных пользователей.

    SessionAuthentication в DRF проверяет CSRF только у уже вошедших пользователей,
    поэтому анонимные POST (вход, регистрация, подписка) нужно проверять явно.
    """

    csrf_actions: frozenset[str] = frozenset()

    def initial(self, request: Request, *args, **kwargs) -> None:
        super().initial(request, *args, **kwargs)
        if self.action in self.csrf_actions:
            SessionAuthentication().enforce_csrf(request)

from django.db import connection
from django.http import HttpRequest, JsonResponse


def healthcheck_view(request: HttpRequest) -> JsonResponse:
    """Проверка, что приложение запущено и база отвечает."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})

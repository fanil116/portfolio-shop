from rest_framework.routers import SimpleRouter

from users.viewsets import AuthViewSet

router = SimpleRouter()

router.register("auth", AuthViewSet, "auth")

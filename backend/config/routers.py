from rest_framework.routers import SimpleRouter

from catalog.viewsets import CategoryViewSet
from content.viewsets import HomeViewSet, SiteViewSet
from newsletter.viewsets import NewsletterViewSet
from users.viewsets import AuthViewSet

router = SimpleRouter()

router.register("auth", AuthViewSet, "auth")
router.register("site", SiteViewSet, "site")
router.register("home", HomeViewSet, "home")
router.register("catalog/categories", CategoryViewSet, "categories")
router.register("newsletter", NewsletterViewSet, "newsletter")

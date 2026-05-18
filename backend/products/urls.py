from rest_framework.routers import DefaultRouter

from .views import (
    ConfigurationProjectViewSet,
    ControllerViewSet,
    ProductFamilyViewSet,
    ProductVariantViewSet,
)

router = DefaultRouter()
#aqui vemos que url llama a que vista
# El router convierte cada ViewSet en endpoints REST: list, detail, create, etc.
router.register("led-models", ProductFamilyViewSet, basename="led-model")
router.register("led-variants", ProductVariantViewSet, basename="led-variant")
router.register("controllers", ControllerViewSet, basename="controller")
router.register("projects", ConfigurationProjectViewSet, basename="project")

# Backward-compatible read-only alias for the first frontend experiment.
router.register("products", ProductVariantViewSet, basename="product")

urlpatterns = router.urls

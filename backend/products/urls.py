from rest_framework.routers import DefaultRouter
#conecta rutas API con ViewSets
''' FLUJO ACTUAL DEL PROYECTO
Django Admin
  ↓
creas datos LED
  ↓
SQLite guarda:
    ProductFamily
    ProductVariant
    Controller
    UserProfile
    ConfigurationProject
  ↓
DRF expone API
  ↓
Nuxt pide datos
  ↓
Nuxt muestra:
    modal de modelos
    tabla de variantes
    configurador
    especificaciones'''
from .views import (
    ConfigurationProjectViewSet,
    ControllerViewSet,
    ProductFamilyViewSet,
    ProductVariantViewSet,
)

router = DefaultRouter()
router.register("led-models", ProductFamilyViewSet, basename="led-model")
router.register("led-variants", ProductVariantViewSet, basename="led-variant")
router.register("controllers", ControllerViewSet, basename="controller")
router.register("projects", ConfigurationProjectViewSet, basename="project")

# Backward-compatible read-only alias for the first frontend experiment.
router.register("products", ProductVariantViewSet, basename="product")

urlpatterns = router.urls

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.db.models import Count, Prefetch, Q
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConfigurationProject, Controller, ProductFamily, ProductVariant
from .serializers import (
    AuthUserSerializer,
    ConfigurationProjectSerializer,
    ControllerSerializer,
    LoginSerializer,
    ProductFamilyDetailSerializer,
    ProductFamilyListSerializer,
    ProductVariantSerializer,
    RegisterSerializer,
)


class ProductFamilyViewSet(viewsets.ReadOnlyModelViewSet):
    # Atiende /api/led-models/ y /api/led-models/{slug}/.
    # En detalle cambia de serializer para incluir variantes.
    lookup_field = "slug"

    def get_queryset(self):
        # Prefetch evita consultas extra cuando el detalle serializa variants.
        active_variants = ProductVariant.objects.filter(is_active=True).order_by(
            "display_order",
            "pixel_pitch",
        )
        return (
            ProductFamily.objects.filter(is_active=True)
            .annotate(variants_count=Count("variants", filter=Q(variants__is_active=True)))
            .prefetch_related(Prefetch("variants", queryset=active_variants))
            .order_by("display_order", "name")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductFamilyDetailSerializer
        return ProductFamilyListSerializer


class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    # Atiende /api/led-variants/. Permite filtrar por tipo o familia desde Nuxt.
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        queryset = (
            ProductVariant.objects.filter(is_active=True, family__is_active=True)
            .select_related("family")
            .order_by("family__display_order", "family__name", "display_order", "pixel_pitch")
        )

        product_type = self.request.query_params.get("product_type")
        family_slug = self.request.query_params.get("family")

        if product_type:
            queryset = queryset.filter(family__product_type=product_type)
        if family_slug:
            queryset = queryset.filter(family__slug=family_slug)

        return queryset


class ControllerViewSet(viewsets.ReadOnlyModelViewSet):
    # Atiende /api/controllers/. Los precios los protege ControllerSerializer.
    serializer_class = ControllerSerializer

    def get_queryset(self):
        return Controller.objects.filter(is_active=True).order_by("display_order", "brand", "name")


class ConfigurationProjectViewSet(viewsets.ModelViewSet):
    # Atiende /api/projects/. Es el unico endpoint actual que requiere login
    # porque cada configuracion pertenece a un usuario.
    serializer_class = ConfigurationProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = (
            ConfigurationProject.objects.select_related(
                "selected_variant",
                "selected_variant__family",
                "controller",
                "user",
            )
            .all()
            .order_by("-updated_at", "-created_at")
        )

        user = self.request.user
        # Staff puede revisar todos los proyectos; usuarios normales solo ven los suyos.
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(user=user)


def auth_response(user, request):
    return {
        "user": AuthUserSerializer(user, context={"request": request}).data,
        "csrf_token": get_token(request),
    }


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CurrentUserView(APIView):
    # /auth/me/ tambien deja preparada la cookie CSRF para los POST con sesion.
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"user": None, "csrf_token": get_token(request)})

        return Response(auth_response(request.user, request))


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Aqui Django crea la sesion del usuario tras validar email/password.
        user = serializer.validated_data["user"]
        django_login(request, user)

        return Response(auth_response(user, request), status=status.HTTP_200_OK)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # En esta fase sin email verification, registramos y dejamos la sesion iniciada.
        django_login(request, user)

        return Response(auth_response(user, request), status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

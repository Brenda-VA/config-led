from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Controller, ProductFamily, ProductVariant


class AuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user_profile_and_session(self):
        response = self.client.post(
            "/auth/register/",
            {
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
                "company": "Synetech",
                "country": "Spain",
                "phone": "+34123456789",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"]["email"], "new@example.com")
        self.assertFalse(response.data["user"]["can_view_prices"])

        user = get_user_model().objects.get(email="new@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.price_profile.company, "Synetech")

        me_response = self.client.get("/auth/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["user"]["email"], "new@example.com")

    def test_login_and_logout(self):
        get_user_model().objects.create_user(
            username="login@example.com",
            email="login@example.com",
            password="StrongPass123!",
        )

        login_response = self.client.post(
            "/auth/login/",
            {"email": "login@example.com", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.data["user"]["email"], "login@example.com")

        logout_response = self.client.post("/auth/logout/")
        self.assertEqual(logout_response.status_code, 204)

        me_response = self.client.get("/auth/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertIsNone(me_response.data["user"])


class PermissionAndProjectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.controller = Controller.objects.create(
            brand=Controller.NOVASTAR,
            name="VX1000",
            price=Decimal("1200.00"),
        )
        self.family = ProductFamily.objects.create(
            name="Immersif",
            slug="immersif",
            product_type=ProductFamily.INDOOR,
        )
        self.variant = ProductVariant.objects.create(
            family=self.family,
            model_name="Immersif COB 1.2",
            pixel_pitch=Decimal("1.20"),
            brightness_nits=600,
            cabinet_width_mm=Decimal("600.00"),
            cabinet_height_mm=Decimal("337.50"),
            cabinet_depth_mm=Decimal("39.00"),
            cabinet_weight_kg=Decimal("8.50"),
            refresh_rate_hz=3840,
            web_price_per_cabinet=Decimal("900.00"),
            resolution_width_px_per_cabinet=500,
            resolution_height_px_per_cabinet=281,
            max_power_w=Decimal("180.00"),
            typical_power_w=Decimal("90.00"),
            max_heat_btu_h=Decimal("614.16"),
            typical_heat_btu_h=Decimal("307.08"),
        )

    def test_prices_are_hidden_until_user_has_permission(self):
        response = self.client.get("/api/controllers/")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data[0]["price"])

        user = get_user_model().objects.create_user(
            username="price@example.com",
            email="price@example.com",
            password="StrongPass123!",
        )
        user.price_profile.can_view_prices = True
        user.price_profile.save(update_fields=["can_view_prices"])
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/controllers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["price"], "1200.00")

    def test_project_save_requires_authentication(self):
        response = self.client.post("/api/projects/", {}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_save_project(self):
        user = get_user_model().objects.create_user(
            username="project@example.com",
            email="project@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/projects/",
            {
                "name": "Test project",
                "selected_variant": self.variant.id,
                "controller": self.controller.id,
                "wall_width_m": "5.00",
                "wall_height_m": "3.00",
                "columns": 2,
                "rows": 2,
                "unit": "m",
                "resolution_preset": "FHD",
                "redundancy": "none",
                "content_mode": "default_image",
                "custom_image_path": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_cabinets"], 4)
        self.assertEqual(response.data["calculated_resolution_width"], 1000)

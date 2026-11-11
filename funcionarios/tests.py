import re

from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from .models import Funcionario


class IniciarSesionFuncionarioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "ClaveSegura-de-prueba-2026"
        cls.funcionario = Funcionario.objects.create_user(
            rut="12345678-5",
            password=cls.password,
            email="funcionario@example.com",
            first_name="Ana",
            last_name="Prueba",
        )

    def test_inicia_sesion_con_correo(self):
        response = self.client.post(
            reverse("funcionario:iniciar_sesion"),
            {
                "identificador": self.funcionario.email.upper(),
                "password": self.password,
            },
        )
        self.assertRedirects(response, reverse("funcionario:funcionario"))

    def test_inicia_sesion_con_rut_con_puntos(self):
        response = self.client.post(
            reverse("funcionario:iniciar_sesion"),
            {
                "identificador": "12.345.678-5",
                "password": self.password,
            },
        )
        self.assertRedirects(response, reverse("funcionario:funcionario"))


class DesactivacionMasivaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Funcionario.objects.create_superuser(
            rut="11111111-1",
            password="ClaveSegura-de-prueba-2026",
            email="admin@example.com",
            first_name="Admin",
            last_name="Prueba",
        )
        cls.funcionarios = [
            Funcionario.objects.create_user(
                rut=rut,
                password="ClaveSegura-de-prueba-2026",
                email=f"{index}@example.com",
                first_name="Funcionario",
                last_name=str(index),
            )
            for index, rut in enumerate(("12345678-5", "22222222-2"), start=1)
        ]

    def test_superusuario_desactiva_varios_funcionarios_sin_desactivarse(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("funcionario:funcionario"),
            {
                "accion": "desactivar",
                "funcionarios": [user.pk for user in self.funcionarios]
                + [self.admin.pk, "no-es-un-id", str(2**100)],
            },
        )

        self.assertRedirects(response, reverse("funcionario:funcionario"))
        self.assertFalse(
            Funcionario.objects.filter(
                pk__in=[user.pk for user in self.funcionarios], is_active=True
            ).exists()
        )
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_usuario_no_administrador_no_puede_desactivar_usuarios(self):
        self.client.force_login(self.funcionarios[0])

        response = self.client.post(
            reverse("funcionario:funcionario"),
            {"accion": "desactivar", "funcionarios": [self.funcionarios[1].pk]},
        )

        self.assertEqual(response.status_code, 403)
        self.funcionarios[1].refresh_from_db()
        self.assertTrue(self.funcionarios[1].is_active)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class RecuperarContrasenaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.funcionario = Funcionario.objects.create_user(
            rut="12345678-5",
            password="ClaveSegura-de-prueba-2026",
            email="funcionario@example.com",
            first_name="Ana",
            last_name="Prueba",
        )

    def test_usuario_puede_cambiar_contrasena_desde_el_enlace(self):
        response = self.client.post(
            reverse("funcionario:password_reset"),
            {"email": self.funcionario.email},
        )
        self.assertRedirects(response, reverse("funcionario:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)

        match = re.search(
            r"http://testserver/funcionario/restablecerContrasena/([\w-]+)/([\w-]+)/",
            mail.outbox[0].body,
        )
        self.assertIsNotNone(match)
        uidb64, token = match.groups()
        reset_url = reverse(
            "funcionario:password_reset_confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )
        response = self.client.get(reset_url, follow=True)
        self.assertEqual(response.status_code, 200)

        new_password = "Nueva-Clave-segura-2026!"
        response = self.client.post(
            response.request["PATH_INFO"],
            {
                "new_password1": new_password,
                "new_password2": new_password,
            },
        )

        self.assertRedirects(response, reverse("funcionario:password_reset_complete"))
        self.funcionario.refresh_from_db()
        self.assertTrue(self.funcionario.check_password(new_password))

    def test_correo_no_registrado_muestra_confirmacion_generica(self):
        response = self.client.post(
            reverse("funcionario:password_reset"),
            {"email": "desconocido@example.com"},
        )

        self.assertRedirects(response, reverse("funcionario:password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

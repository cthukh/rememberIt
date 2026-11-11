"""Pruebas funcionales de autenticación para el módulo funcionarios.

Se ejecutan con el runner de Django y usan la base de datos de pruebas
configurada en settings.py (Oracle en este proyecto). Django crea y destruye
la base de datos de pruebas; no se deben usar datos reales de producción.
"""

import re
from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.sessions.models import Session
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone


Funcionario = get_user_model()


class AutenticacionFuncionarioTests(TestCase):
    """Login válido e inválido, y acceso a vistas protegidas."""

    password = "ClaveSegura-de-prueba-2026"

    @classmethod
    def setUpTestData(cls):
        cls.funcionario = Funcionario.objects.create_user(
            rut="12345678-5",
            password=cls.password,
            email="funcionario@example.com",
            first_name="Ana",
            last_name="Prueba",
        )

    def login_url(self):
        return reverse("funcionario:iniciar_sesion")

    def enviar_login(self, identificador, password=None):
        return self.client.post(
            self.login_url(),
            {
                "identificador": identificador,
                "password": self.password if password is None else password,
            },
        )

    def test_login_correcto_con_rut_inicia_sesion(self):
        response = self.enviar_login("12.345.678-5")

        self.assertRedirects(
            response,
            reverse("funcionario:funcionario"),
            fetch_redirect_response=False,
        )
        self.assertEqual(
            str(self.client.session[SESSION_KEY]), str(self.funcionario.pk)
        )

    def test_login_correcto_con_correo_inicia_sesion(self):
        response = self.enviar_login(self.funcionario.email)

        self.assertRedirects(
            response,
            reverse("funcionario:funcionario"),
            fetch_redirect_response=False,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_login_rechaza_contrasena_incorrecta(self):
        response = self.enviar_login(
            self.funcionario.rut, password="Contrasena-incorrecta-2026"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "El correo/RUT o la contraseña no son correctos."
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_login_rechaza_usuario_inexistente(self):
        response = self.enviar_login("11111111-1")

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "El correo/RUT o la contraseña no son correctos."
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_vista_protegida_redirige_si_no_hay_sesion(self):
        protected_url = reverse("funcionario:funcionario")
        response = self.client.get(protected_url)

        self.assertRedirects(
            response,
            f"{self.login_url()}?next={protected_url}",
            fetch_redirect_response=False,
        )

    def test_cerrar_sesion_impide_volver_a_vista_protegida(self):
        self.enviar_login(self.funcionario.rut)
        response = self.client.get(reverse("funcionario:cerrar_sesion"))

        self.assertRedirects(
            response, self.login_url(), fetch_redirect_response=False
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
        protected_url = reverse("funcionario:funcionario")
        response = self.client.get(protected_url)
        self.assertRedirects(
            response,
            f"{self.login_url()}?next={protected_url}",
            fetch_redirect_response=False,
        )


class RecuperacionContrasenaTests(TestCase):
    """Comprueba el flujo de recuperación por correo y el uso de la nueva clave."""

    password = "ClaveSegura-de-prueba-2026"
    nueva_password = "NuevaClave-Segura-2026!"

    @classmethod
    def setUpTestData(cls):
        cls.funcionario = Funcionario.objects.create_user(
            rut="12345678-5",
            password=cls.password,
            email="funcionario@example.com",
            first_name="Ana",
            last_name="Prueba",
        )

    def test_recuperacion_envia_correo_solo_para_cuenta_existente(self):
        response = self.client.post(
            reverse("funcionario:password_reset"),
            {"email": self.funcionario.email},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.funcionario.email, mail.outbox[0].to)
        self.assertIn("restablecerContrasena/", mail.outbox[0].body)

    def test_recuperacion_no_revela_cuentas_inexistentes(self):
        response = self.client.post(
            reverse("funcionario:password_reset"),
            {"email": "no-existe@example.com"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

    def test_enlace_valido_cambia_contrasena_y_permite_nuevo_login(self):
        self.client.post(
            reverse("funcionario:password_reset"),
            {"email": self.funcionario.email},
        )
        self.assertEqual(len(mail.outbox), 1)

        match = re.search(
            r"/funcionario/restablecerContrasena/([^/]+)/([^/\s]+)",
            mail.outbox[0].body,
        )
        self.assertIsNotNone(match, "El correo debe incluir el enlace de recuperación")
        uidb64, token = match.groups()
        confirm_url = reverse(
            "funcionario:password_reset_confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )

        # Django cambia el token de la URL por 'set-password' tras validar el enlace.
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 302)
        parsed = urlparse(response.url)
        confirm_path = parsed.path
        response = self.client.post(
            confirm_path,
            {
                "new_password1": self.nueva_password,
                "new_password2": self.nueva_password,
            },
        )
        self.assertRedirects(
            response,
            reverse("funcionario:password_reset_complete"),
            fetch_redirect_response=False,
        )

        self.funcionario.refresh_from_db()
        self.assertTrue(self.funcionario.check_password(self.nueva_password))
        self.assertFalse(self.funcionario.check_password(self.password))
        self.assertTrue(
            self.client.login(
                rut=self.funcionario.rut, password=self.nueva_password
            )
        )

    def test_enlace_de_recuperacion_con_token_invalido_no_permite_cambiar_clave(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        uidb64 = urlsafe_base64_encode(force_bytes(self.funcionario.pk))
        invalid_url = reverse(
            "funcionario:password_reset_confirm",
            kwargs={"uidb64": uidb64, "token": "token-invalido"},
        )
        response = self.client.get(invalid_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restablecer")
        self.assertNotContains(response, 'name="new_password1"')


class TimeoutSesionTests(TestCase):
    """Comprueba configuración y expiración de sesiones en la BD de Django."""

    password = "ClaveSegura-de-prueba-2026"

    @classmethod
    def setUpTestData(cls):
        cls.funcionario = Funcionario.objects.create_user(
            rut="12345678-5",
            password=cls.password,
            email="funcionario@example.com",
            first_name="Ana",
            last_name="Prueba",
        )

    def iniciar_sesion(self):
        return self.client.post(
            reverse("funcionario:iniciar_sesion"),
            {"identificador": self.funcionario.rut, "password": self.password},
        )

    def test_configuracion_define_timeout_de_quince_minutos(self):
        self.assertEqual(settings.SESSION_COOKIE_AGE, 15 * 60)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)

    def test_sesion_activa_renueva_vencimiento_en_una_peticion(self):
        self.iniciar_sesion()
        session_key = self.client.session.session_key
        self.assertIsNotNone(session_key)
        sesion_antes = Session.objects.get(session_key=session_key)

        response = self.client.get(reverse("funcionario:funcionario"))
        self.assertEqual(response.status_code, 200)

        sesion_despues = Session.objects.get(session_key=session_key)
        self.assertGreaterEqual(sesion_despues.expire_date, sesion_antes.expire_date)
        self.assertEqual(
            int(response.cookies[settings.SESSION_COOKIE_NAME]["max-age"]),
            settings.SESSION_COOKIE_AGE,
        )

    def test_sesion_expirada_en_base_de_datos_exige_nuevo_login(self):
        self.iniciar_sesion()
        session_key = self.client.session.session_key
        Session.objects.filter(session_key=session_key).update(
            expire_date=timezone.now() - timedelta(seconds=1)
        )

        protected_url = reverse("funcionario:funcionario")
        response = self.client.get(protected_url)
        self.assertRedirects(
            response,
            f"{reverse('funcionario:iniciar_sesion')}?next={protected_url}",
            fetch_redirect_response=False,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

from __future__ import annotations

from playwright.sync_api import expect
from .base_page import BasePage

class LoginPage(BasePage):
    PATH = "/login"
    def __init__(self, page, settings):
        super().__init__(page, settings)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def email(self):
        return self.page.locator(
            "input[name='username'], "
            "input[type='email'], "
            "input[autocomplete='email'], "
            "input[placeholder*='адрес' i], "
            "input[placeholder*='email' i]"
        )

    @property
    def password(self):
        return self.page.locator(
            "input[name='password'], "
            "input[type='password'], "
            "input[autocomplete='current-password'], "
            "input[placeholder*='пароль' i]"
        )

    @property
    def submit(self):
        return self.page.locator(
            "[data-cy='login-submit'], "
            "button[type='submit']:has-text('Войти')"
        )

    def assert_loaded(self, timeout: int = 20000) -> "LoginPage":
        expect(self.email.first).to_be_visible(timeout=timeout)
        expect(self.password.first).to_be_visible(timeout=timeout)
        expect(self.submit.first).to_be_visible(timeout=timeout)
        return self

    def fill_credentials(self) -> "LoginPage":
        username = getattr(self.settings, "username", None)
        password = getattr(self.settings, "password", None)
        # на всякий случай очистим и заполним
        self.email.first.fill("")
        self.email.first.fill(username)
        self.password.first.fill("")
        self.password.first.fill(password)
        return self

    def submit_login(self) -> "LoginPage":
        self.submit.first.click()
        return self

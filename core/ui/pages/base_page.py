from __future__ import annotations
import allure
from playwright.sync_api import expect

class BasePage:
    URL: str | None = None

    def __init__(self, page, settings=None):
        self.page = page
        self.settings = settings

    @property
    def sidebar(self):
        return self.page.locator(
            "[data-cy='sidebar']"
        )

    @property
    def logo(self):
        return self.page.locator(
            "[data-cy='product-logo']"
        )

    @property
    def toast_error(self):
        return self.page.locator(
            "[data-cy='toast-error']"
        )

    @property
    def toast_success(self):
        return self.page.locator(
            "[data-cy='toast-success']"
        )

    @property
    def page_content(self):
        return self.page.locator(
            "[data-cy='page-content']"
        )

    @property
    def user_menu(self):
        return self.page.locator(
            "[data-cy='toggle-user-menu']"
        )

    @property
    def logout_button(self):
        return self.page.locator(
            "[data-cy='logout']"
        )

    def open(self, url: str | None = None):
        target = url or self.URL
        assert target, "URL must be provided for .open()"
        with allure.step(f"OPEN {target}"):
            self.page.goto(target, wait_until="domcontentloaded", timeout=30000)
        return self

    def screenshot(self, name: str = "page") -> None:
        self.page.screenshot(path=f"{name}.png", full_page=False)
        allure.attach.file(f"{name}.png", name=name, attachment_type=allure.attachment_type.PNG)

    @staticmethod
    def scroll_to_bottom(locator):
        locator.press("End")

    @staticmethod
    def assert_field_value_is_equal(locator, value):
        expect(locator).to_have_value(value)

    @staticmethod
    def assert_all_texts_in_elements_are_equal(locator, expected_text):
        expect(locator).not_to_have_count(0)
        texts = locator.all_inner_texts()
        assert all(
            text == expected_text for text in texts), f"Expected all texts to be '{expected_text}', but got: {texts}"

    @staticmethod
    def assert_all_texts_in_elements_contain(locator, expected_text):
        expect(locator).not_to_have_count(0)
        texts = locator.all_inner_texts()
        assert all(
            expected_text in text for text in texts), f"Expected all texts to be '{expected_text}', but got: {texts}"

    @staticmethod
    def click_item_by_text(locator, text):
        expect(locator.first).to_be_visible()
        count = locator.count()

        for i in range(count):
            item = locator.nth(i)
            if item.inner_text() == text:
                item.click()
                return

        raise AssertionError(f"Element with text '{text}' is not found")

    @staticmethod
    def select_element_by_text(locator, text):
        return locator.filter(has_text=text).first

    @staticmethod
    def assert_element_not_present_by_text(locator, text):
        expect(locator.filter(has_text=text)).to_have_count(0, timeout=5000)

    @staticmethod
    def assert_element_name_is_equal(locator, name):
        expect(locator.filter(has_text=name)).to_be_visible()

    def assert_logged_in(self):
        expect(self.sidebar).to_be_visible()

    def assert_no_toast_error(self):
        expect(self.toast_error).not_to_be_visible()

    def assert_toast_success(self):
        expect(self.toast_success.first).to_be_visible()
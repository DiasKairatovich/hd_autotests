from core.ui.pages.base_page import BasePage


class UsersPage(BasePage):
    PATH = "/users"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_user_button(self):
        return self.page.locator(
            "[data-cy='new-user-button']"
        )

    @property
    def user_cards(self):
        return self.page.locator(
            "[data-cy='user-item']"
        )

    @property
    def search_input_field(self):
        return self.page.locator(
            "[data-cy='user-search-input']"
        )

    @property
    def edit_user_button(self):
        return self.page.locator(
            "[data-cy='user-edit-link']"
        )

    @property
    def delete_user_button(self):
        return self.page.locator(
            "[data-cy='user-delete-button']"
        )

    @property
    def delete_user_confirm_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )

    @property
    def user_name_input_field(self):
        return self.page.locator(
            "[data-cy='first-name-input']"
        )

    @property
    def user_last_name_input_field(self):
        return self.page.locator(
            "[data-cy='last-name-input']"
        )

    @property
    def user_email_input_field(self):
        return self.page.locator(
            "[data-cy='email-input']"
        )

    @property
    def user_role_dropdown(self):
        return self.page.locator(
            "[data-cy='role-toggle-button']"
        )

    @property
    def user_role_options(self):
        return self.page.locator(
            "[data-cy='role-option']"
        )

    @property
    def add_user_submit_button(self):
        return self.page.locator(
            "[data-cy='new-user-submit']"
        )

    @property
    def edit_user_submit_button(self):
        return self.page.locator(
            "[data-cy='edit-user-submit']"
        )

    @property
    def user_groups_dropdown(self):
        return self.page.locator(
            "[data-cy='groups-multibox-input']"
        )

    @property
    def user_group_options(self):
        return self.page.locator(
            "[data-cy='groups-option']"
        )

    @property
    def generate_password_button(self):
        return self.page.locator(
            "button:has(use[href*='Secure'])"
        )
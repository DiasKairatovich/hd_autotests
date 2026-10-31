from core.ui.pages.base_page import BasePage


class WebhooksPage(BasePage):
    PATH = "/webhooks"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_webhook_button(self):
        return self.page.locator(
            "[data-cy='webhooks-new-button']"
        )

    @property
    def webhook_cards(self):
        return self.page.locator(
            "[data-cy='webhook-item']"
        )

    @property
    def webhook_name_field_in_modal(self):
        return self.page.locator(
            "[data-cy='name-input']"
        )

    @property
    def webhook_url_field_in_modal(self):
        return self.page.locator(
            "[data-cy='url-input']"
        )

    @property
    def webhook_subscription_dropdown_in_modal(self):
        return self.page.locator(
            "[data-cy='subscription-toggle-button']"
        )

    @property
    def webhook_subscription_option_in_dropdown(self):
        return self.page.locator(
            "[data-cy='subscription-option'][aria-disabled='false']"
        )

    @property
    def save_webhook_button(self):
        return self.page.locator(
            "[data-cy='webhook-submit-button']"
        )

    @property
    def edit_button(self):
        return self.page.locator(
            "[data-cy='webhook-edit-button']"
        )

    @property
    def delete_button(self):
        return self.page.locator(
            "[data-cy='webhook-delete-button']"
        )

    @property
    def confirm_delete_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )
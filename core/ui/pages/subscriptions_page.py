from core.ui.pages.base_page import BasePage


class SubscriptionsPage(BasePage):
    PATH = "/subscriptions"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_subscription_button(self):
        return self.page.locator(
            "[data-cy='new-subscription-link']"
        )

    @property
    def tab_subscriptions(self):
        return self.page.locator(
            "[data-cy='tab-subscriptions']"
        )

    @property
    def tab_situations(self):
        return self.page.locator(
            "[data-cy='tab-situations']"
        )

    @property
    def subscription_items(self):
        return self.page.locator(
            "[data-cy='subscription-item']"
        )

    @property
    def situation_items(self):
        return self.page.locator(
            "[data-cy='situation-row']"
        )

    @property
    def edit_subscription_button(self):
        return self.page.locator(
            "[data-cy='subscription-edit-link']"
        )

    @property
    def delete_subscription_button(self):
        return self.page.locator(
            "[data-cy='subscription-delete-button']"
        )

    @property
    def search_situation_field(self):
        return self.page.locator(
            "[data-cy='situation-search-input']"
        )

    @property
    def subscription_name_field(self):
        return self.page.locator(
            "[name='name']"
        )

    @property
    def subscription_camera_dropdown(self):
        return self.page.locator(
            "[data-cy='camera-combobox-input']"
        )

    @property
    def subscription_camera_options(self):
        return self.page.locator(
            "[data-cy='camera-option']"
        )

    @property
    def subscription_save_confirm_button(self):
        return self.page.locator(
            "[data-cy='subscription-save-button']"
        )

    @property
    def subscription_delete_confirm_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )
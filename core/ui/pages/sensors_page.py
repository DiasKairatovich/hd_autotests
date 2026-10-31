from core.ui.pages.base_page import BasePage


class SensorsPage(BasePage):
    PATH = "/sensors"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_sensor_button(self):
        return self.page.locator(
            "[data-cy='sensor-create-button']"
        )

    @property
    def search_sensor_field(self):
        return self.page.locator(
            "[data-cy='sensor-search-input']"
        )

    @property
    def sensor_cards(self):
        return self.page.locator(
            "[data-cy='sensor-row']"
        )

    @property
    def edit_sensor_button(self):
        return self.page.locator(
            "[data-cy='sensor-edit-button']"
        )

    @property
    def delete_sensor_button(self):
        return self.page.locator(
            "[data-cy='sensor-delete-button']"
        )

    @property
    def sensor_delete_confirm_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )

    @property
    def sensor_name_field_in_modal(self):
        return self.page.locator(
            "[data-cy='sensor-name-input']"
        )

    @property
    def sensor_kinds_dropdown(self):
        return self.page.locator(
            "[data-cy='sensor-kind-combobox-input']"
        )

    @property
    def sensor_kinds_options(self):
        return self.page.locator(
            "[data-cy='sensor-kind-option']"
        )

    @property
    def sensor_place_dropdown(self):
        return self.page.locator(
            "[data-cy='sensor-place-picker-trigger']"
        )

    @property
    def sensor_place_search_field(self):
        return self.page.locator(
            "[data-cy='place-search-input']"
        )

    @property
    def sensor_place_items(self):
        return self.page.locator(
            "[data-cy='place-picker-item']"
        )

    @property
    def sensor_place_submit_button(self):
        return self.page.locator(
            "[data-cy='place-complex-picker-submit-button']"
        )

    @property
    def camera_sensor_dropdown(self):
        return self.page.locator(
            "[data-cy='sensor-form'] [data-cy='camera-combobox-input']"
        )

    @property
    def camera_sensor_options(self):
        return self.page.locator(
            "[data-cy='camera-option']"
        )

    @property
    def add_sensor_submit_button(self):
        return self.page.locator(
            "[data-cy='new-sensor-submit-button']"
        )

    @property
    def edit_sensor_submit_button(self):
        return self.page.locator(
            "[data-cy='edit-sensor-submit-button']"
        )

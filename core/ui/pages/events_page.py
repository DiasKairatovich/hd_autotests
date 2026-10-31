from core.ui.pages.base_page import BasePage


class EventsPage(BasePage):
    PATH = "/events"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def tab_filter(self):
        return self.page.locator(
            "[data-cy='tab-filter']"
        )

    @property
    def tab_subscription(self):
        return self.page.locator(
            "[data-cy='tab-subscription']"
        )

    @property
    def tab_sensor(self):
        return self.page.locator(
            "[data-cy='tab-sensorreadings']"
        )

    @property
    def tab_search(self):
        return self.page.locator(
            "[data-cy='tab-search']"
        )

    @property
    def panel_filter(self):
        return self.page.locator(
            "[id='panel-filter'] > div:first-child"
        )

    @property
    def group_dropdown(self):
        return self.page.locator(
            "[data-cy='group-combobox-input']"
        )

    @property
    def camera_dropdown(self):
        return self.page.locator(
            "[data-cy='camera-combobox-input']"
        )

    @property
    def list_dropdown(self):
        return self.page.locator(
            "[data-cy='superlist-combobox-input']"
        )

    @property
    def place_dropdown(self):
        return self.page.locator(
            "[data-cy='place-picker-trigger']"
        )

    @property
    def event_type_dropdown(self):
        return self.page.locator(
            "[data-cy='event-type-toggle-button']"
        )

    @property
    def event_list(self):
        return self.page.locator(
            "[data-cy='event-list']"
        )

    @property
    def event_list_item(self):
        return self.page.locator(
            "[data-cy='event-list-item']"
        )
from playwright.sync_api import expect

from core.ui.pages.base_page import BasePage

class MapPage(BasePage):
    PATH = "/map"
    def __init__(self, page, settings):
        super().__init__(page)
        self.page = page
        self.URL = settings.ui_base_url + self.PATH

    @property
    def map(self):
        return self.page.locator(
            "[aria-label='Map']"
        )

    @property
    def zoom_in_button(self):
        return self.page.locator(
            "[title='Zoom in']"
        )

    @property
    def zoom_out_button(self):
        return self.page.locator(
            "[title='Zoom out']"
        )

    @property
    def compass_button(self):
        return self.page.locator(
            "[title='Reset bearing to north']"
        )

    @property
    def location_button(self):
        return self.page.locator(
            "[title='Find my location']"
        )

    @property
    def tags_tub(self):
        return self.page.locator(
            "[data-cy='tab-tags']"
        )

    @property
    def categories_tub(self):
        return self.page.locator(
            "[data-cy='tab-categories']"
        )

    @property
    def map_search_field(self):
        return self.page.locator(
            "[data-cy='map-search-input']"
        )

    def check_page_elements(self):
        expect(self.map).to_be_visible()
        expect(self.zoom_in_button).to_be_visible()
        expect(self.zoom_out_button).to_be_visible()
        expect(self.compass_button).to_be_visible()
        expect(self.location_button).to_be_visible()
        expect(self.tags_tub).to_be_visible()
        expect(self.categories_tub).to_be_visible()
        expect(self.map_search_field).to_be_visible()
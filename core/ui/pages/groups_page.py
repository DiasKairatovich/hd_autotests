from core.ui.pages.base_page import BasePage


class GroupsPage(BasePage):
    PATH = "/groups"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_group_button(self):
        return self.page.locator(
            "[data-cy='groups-new-button']"
        )

    @property
    def search_field(self):
        return self.page.locator(
            "[data-cy='group-search-input']"
        )

    @property
    def group_cards(self):
        return self.page.locator(
            "[data-cy='groups-item']"
        )

    @property
    def edit_group_button(self):
        return self.page.locator(
            "[data-cy='groups-item-edit']"
        )

    @property
    def delete_group_button(self):
        return self.page.locator(
            "[data-cy='group-delete-button']"
        )

    @property
    def name_field_in_create_modal(self):
        return self.page.locator(
            "[data-cy='groups-new-name-input']"
        )

    @property
    def name_field_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='groups-edit-name-input']"
        )

    @property
    def title_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='page-content'] h1"
        )

    @property
    def submit_button_in_create_modal(self):
        return self.page.locator(
            "[data-cy='group-submit-button']"
        )

    @property
    def submit_button_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='groups-edit-submit']"
        )

    @property
    def confirm_delete_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )
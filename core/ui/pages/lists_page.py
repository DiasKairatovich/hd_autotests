from core.ui.pages.base_page import BasePage

class ListsPage(BasePage):
    PATH = "/lists"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def add_list_button(self):
        return self.page.locator(
            "[data-cy='new-list-link']"
        )

    @property
    def tab_plates(self):
        return self.page.locator(
            "[data-cy='tab-plate']"
        )

    @property
    def tab_faces(self):
        return self.page.locator(
            "[data-cy='tab-face']"
        )

    @property
    def search_face_lists(self):
        return self.page.locator(
            "[data-cy='facelist-search-input']"
        )

    @property
    def search_plate_lists(self):
        return self.page.locator(
            "[data-cy='platelist-search-input']"
        )

    @property
    def name_field_in_modal(self):
        return self.page.locator(
            "[name='name']"
        )

    @property
    def submit_button_in_modal(self):
        return self.page.locator(
            "[data-cy='form-list-submit']"
        )

    @property
    def face_list_cards(self):
        return self.page.locator(
            "[data-cy='facelist-grid-item']"
        )

    @property
    def plate_list_cards(self):
        return self.page.locator(
            "[data-cy='platelist-grid-item']"
        )

    @property
    def face_list_menu_button(self):
        return self.page.locator(
            "[data-cy='facelist-toggle-button']"
        )

    @property
    def plate_list_menu_button(self):
        return self.page.locator(
            "[data-cy='platelist-toggle-button']"
        )

    @property
    def edit_face_list_button(self):
        return self.page.locator(
            "[data-cy='facelist-option']:nth-of-type(1)"
        )

    @property
    def delete_face_list_button(self):
        return self.page.locator(
            "[data-cy='facelist-option']:nth-of-type(2)"
        )

    @property
    def edit_plate_list_button(self):
        return self.page.locator(
            "[data-cy='platelist-option']:nth-of-type(1)"
        )

    @property
    def delete_plate_list_button(self):
        return self.page.locator(
            "[data-cy='platelist-option']:nth-of-type(2)"
        )

    @property
    def confirm_delete_list_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )
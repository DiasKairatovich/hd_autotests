from core.ui.pages.base_page import BasePage


class PlacesPage(BasePage):
    PATH = "/places"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def places_title(self):
        return self.page.locator(
            "//h1"
        )

    @property
    def add_place_button(self):
        return self.page.locator(
            "[data-cy='new-place-link']"
        )

    @property
    def place_cards(self):
        return self.page.locator(
            "[data-cy='place-row']"
        )

    @property
    def tab_places(self):
        return self.page.locator(
            "[data-cy='tab-places']"
        )

    @property
    def tab_categories(self):
        return self.page.locator(
            "[data-cy='tab-categories']"
        )

    @property
    def tab_kinds(self):
        return self.page.locator(
            "[data-cy='tab-kinds']"
        )

    @property
    def add_category_button(self):
        return self.page.locator(
            "[data-cy='new-placecategory-link']"
        )

    @property
    def category_name_field_in_modal(self):
        return self.page.locator(
            "[data-cy='placecategory-name-input']"
        )

    @property
    def kind_name_field_in_modal(self):
        return self.page.locator(
            "[data-cy='placekind-name-input']"
        )

    @property
    def kinds_dropdown_in_modal(self):
        return self.page.locator(
            "[data-cy='placekind-type-toggle-button']"
        )

    @property
    def kinds_options_in_dropdown(self):
        return self.page.locator(
            "[data-cy='placekind-type-option']"
        )

    @property
    def submit_button_in_kind_modal(self):
        return self.page.locator(
            "[data-cy='placekind-submit-button']"
        )

    @property
    def kind_edit_button(self):
        return self.page.locator(
            "[data-cy='placekind-edit-button']"
        )

    @property
    def kind_delete_button(self):
        return self.page.locator(
            "[data-cy='placekind-delete-button']"
        )

    @property
    def submit_button_in_category_create_modal(self):
        return self.page.locator(
            "[data-cy='new-placecategory-submit-button']"
        )

    @property
    def submit_button_in_category_edit_modal(self):
        return self.page.locator(
            "[data-cy='edit-placecategory-submit-button']"
        )

    @property
    def category_cards(self):
        return self.page.locator(
            "[data-cy='placecategory-node']"
        )

    @property
    def search_categories_field(self):
        return self.page.locator(
            "[data-cy='category-search-input']"
        )

    @property
    def category_search_clear_button(self):
        return self.page.locator(
            "[data-cy='category-search-input'] + div button"
        )

    @property
    def add_kind_button(self):
        return self.page.locator(
            "[data-cy='placekind-create-button']"
        )

    @property
    def place_name_in_create_modal(self):
        return self.page.locator(
            "[data-cy='place-name-input']"
        )

    @property
    def place_group_in_create_modal(self):
        return self.page.locator(
            "[data-cy='place-form'] [data-cy='groups-multibox-input']"
        )

    @property
    def group_options(self):
        return self.page.locator(
            "[data-cy='groups-option']"
        )

    @property
    def submit_button_in_create_modal(self):
        return self.page.locator(
            "[data-cy='new-place-submit']"
        )

    @property
    def submit_button_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='edit-place-submit']"
        )

    @property
    def search_place_field(self):
        return self.page.locator(
            "[data-cy='place-search-input']"
        )

    @property
    def place_menu_button(self):
        return self.page.locator(
            "[data-cy^='place-'][data-cy$='-menu-toggle-button']"
        )

    @property
    def category_menu_button(self):
        return self.page.locator(
            "[data-cy^='placecategory-'][data-cy$='-menu-toggle-button']"
        )

    @property
    def edit_place_button(self):
        return self.page.locator(
            "[data-cy^='place-'][data-cy$='-menu-option']:nth-of-type(1)"
        )

    @property
    def edit_category_button(self):
        return self.page.locator(
            "[data-cy^='placecategory-'][data-cy$='-menu-option']:nth-of-type(1)"
        )

    @property
    def delete_place_button(self):
        return self.page.locator(
            "[data-cy^='place-'][data-cy$='-menu-option']:nth-of-type(2)"
        )

    @property
    def delete_category_button(self):
        return self.page.locator(
            "[data-cy^='placecategory-'][data-cy$='-menu-option']:nth-of-type(4)"
        )

    @property
    def confirm_delete_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )

    @property
    def group_reset_button_in_modal(self):
        return self.page.locator(
            "[data-cy='groups-tag-delete-button']"
        )

    @property
    def kind_cards(self):
        return self.page.locator(
            "//*[@data-cy='placekind-edit-button']/../../.."
        )
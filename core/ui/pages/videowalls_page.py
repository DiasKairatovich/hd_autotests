from core.ui.pages.base_page import BasePage


class VideowallsPage(BasePage):
    PATH = "/videowalls"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def videowalls_title(self):
        return self.page.locator(
            "//h1"
        )

    @property
    def add_videowall_button(self):
        return self.page.locator(
            "[data-cy='new-videowall-button']"
        )

    @property
    def create_videowall_modal(self):
        return self.page.locator(
            "[data-cy='videowall-type-form']"
        )

    @property
    def videowall_name_field_in_create_modal(self):
        return self.page.locator(
            "[name='name']"
        )

    @property
    def videowall_user_field_in_create_modal(self):
        return self.page.locator(
            "[data-cy='user-combobox-input']"
        )

    @property
    def videowall_name_field_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='videowall-name-input']"
        )

    @property
    def videowall_submit_button_in_edit_modal(self):
        return self.page.locator(
            "[data-cy='videowall-save-button']"
        )

    @property
    def user_options(self):
        return self.page.locator(
            "[data-cy='user-option']"
        )

    @property
    def next_button_in_create_modal(self):
        return self.page.locator(
            "[data-cy='new-videowall-setup-layout']"
        )

    @property
    def camera_cards_in_create_grid(self):
        return self.page.locator(
            "[data-cy='videowall-cell-wrapper']"
        )

    @property
    def camera_select_button_in_create_modal(self):
        return self.page.locator(
            "[data-cy='camera-select-button']"
        )

    @property
    def active_camera_items_in_create_modal(self):
        return self.page.locator(
            "[data-cy='camera-item'] img"
        )

    @property
    def add_camera_button_in_create_modal(self):
        return self.page.locator(
            "[data-cy='attach-camera-button']"
        )

    @property
    def save_videowall_button(self):
        return self.page.locator(
            "[data-cy='new-videowall-submit']"
        )

    @property
    def videowall_menu_button(self):
        return self.page.locator(
            "[data-cy='menu-toggle-button']"
        )

    @property
    def delete_button_in_videowall_menu(self):
        return self.page.locator(
            "[data-cy='menu-option']:nth-of-type(2)"
        )

    @property
    def edit_button_in_videowall_menu(self):
        return self.page.locator(
            "[data-cy='menu-option']:nth-of-type(1)"
        )

    @property
    def videowall_search_input(self):
        return self.page.locator(
            "[data-cy='videowalls-search-input']"
        )

    @property
    def videowall_search_clear_button(self):
        return self.page.locator(
            "[data-cy='videowalls-search-input'] + div button"
        )

    @property
    def confirm_delete_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )

    @property
    def videowall_grid_in_create_modal_type1(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type1']"
        )

    @property
    def videowall_grid_in_create_modal_type2(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type2']"
        )

    @property
    def videowall_grid_in_create_modal_type3(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type3']"
        )

    @property
    def videowall_grid_in_create_modal_type4(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type4']"
        )

    @property
    def videowall_grid_in_create_modal_type5(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type5']"
        )

    @property
    def videowall_grid_in_create_modal_type6(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type6']"
        )

    @property
    def videowall_grid_in_create_modal_type7(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type7']"
        )

    @property
    def videowall_grid_in_create_modal_type8(self):
        return self.page.locator(
            "[data-cy='videowall-grid-type8']"
        )

    @property
    def videowall_cards(self):
        return self.page.locator(
            "[data-cy='videowall-card']"
        )

    @property
    def camera_cards_in_videowall(self):
        return self.page.locator(
            "[data-cy^='video-wall-player-grid-']"
        )

    @property
    def videowall_names(self):
        return self.page.locator(
            "[data-cy='videowall-card'] .trhur4b"
        )

    @property
    def edit_videowall_button(self):
        return self.page.locator(
            "[data-cy='edit-videowall-button']"
        )

    def search_videowall_by_name(self, name):
        if self.videowall_search_clear_button.is_visible():
            self.videowall_search_clear_button.click()
        self.videowall_search_input.fill(name)

    def add_cameras_in_create_grid(self):
        count = self.camera_cards_in_create_grid.count()
        for i in range(count):
            self.camera_cards_in_create_grid.nth(i).click()
            self.active_camera_items_in_create_modal.first.click(force=True)
            self.add_camera_button_in_create_modal.click()

    def delete_videowall_by_name(self, name):
        self.search_videowall_by_name(name)
        self.videowall_menu_button.first.click()
        self.delete_button_in_videowall_menu.click()
        self.confirm_delete_button.first.click(force=True)

    def create_new_videowall(self, videowall_name, user_name):
        self.add_videowall_button.click()
        self.videowall_name_field_in_create_modal.fill(videowall_name)
        self.videowall_user_field_in_create_modal.click()
        self.videowall_user_field_in_create_modal.fill(user_name)
        self.user_options.first.evaluate("el => el.click()")
        self.videowall_grid_in_create_modal_type2.click()
        self.next_button_in_create_modal.click()
        self.add_cameras_in_create_grid()
        self.save_videowall_button.click()
        self.assert_toast_success()
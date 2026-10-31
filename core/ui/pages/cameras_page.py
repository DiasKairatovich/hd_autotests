from playwright.sync_api import expect

from core.ui.pages.base_page import BasePage


class CamerasPage(BasePage):
    PATH = "/cameras"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def cameras_title(self):
        return self.page.locator(
            "[data-cy='page-content'] h1"
        )

    @property
    def groups_dropdown(self):
        return self.page.locator(
            "[data-cy='groups-multibox-input']"
        )

    @property
    def groups_options(self):
        return self.page.locator(
            "[data-cy='groups-option']"
        )

    @property
    def places_modal_button(self):
        return self.page.locator(
            "[data-cy='place-picker-trigger']"
        )

    @property
    def reset_place_filter_button(self):
        return self.page.locator(
            "[data-cy='place-picker-trigger'] + div button"
        )

    @property
    def clusters_dropdown(self):
        return self.page.locator(
            "[data-cy='capacitygroup-combobox-input']"
        )

    @property
    def clusters_options(self):
        return self.page.locator(
            "[data-cy='capacitygroup-option']"
        )

    @property
    def video_module_dropdown(self):
        return self.page.locator(
            "[data-cy='video-module-type-toggle-button']"
        )

    @property
    def video_module_options(self):
        return self.page.locator(
            "[data-cy='video-module-type-option']"
        )

    @property
    def reset_video_module_filter_button(self):
        return self.page.locator(
            "[data-cy='video-module-type-reset-button']"
        )

    @property
    def camera_state_dropdown(self):
        return self.page.locator(
            "[data-cy='camera-state-toggle-button']"
        )

    @property
    def camera_state_options(self):
        return self.page.locator(
            "[data-cy='camera-state-option']"
        )

    @property
    def add_tags_buttons(self):
        return self.page.locator(
            "[data-cy='item-tag']"
        )

    @property
    def search_field(self):
        return self.page.locator(
            "[data-cy='camera-search-input']"
        )

    @property
    def search_clear_button(self):
        return self.page.locator(
            "[data-cy='camera-search-input'] ~ div button"
        )

    @property
    def add_camera_button(self):
        return self.page.locator(
            "[data-cy='new-camera-link']"
        )

    @property
    def camera_items(self):
        return self.page.locator(
            "[data-cy='camera-item']"
        )

    @property
    def retry_stream_button(self):
        return self.page.locator(
            "[data-cy='player-failure-retry-button']"
        )

    @property
    def camera_video_modules_in_items(self):
        return self.page.locator(
            "[data-cy='camera-hero'] ._14p0t914"
        )

    @property
    def camera_places_in_items(self):
        return self.page.locator(
            "[data-cy='camera-item'] ._9gutwe0 a"
        )

    @property
    def camera_names_in_items(self):
        return self.page.locator(
            "[data-cy='camera-item'] [title]"
        )

    @property
    def camera_mini_player(self):
        return self.page.locator(
            "[data-cy='mini-player-draggable']"
        )

    @property
    def cameras_overlay_items(self):
        return self.page.locator(
            "[data-cy='camera-item-overlay-button']"
        )

    @property
    def camera_name_in_mini_player(self):
        return self.page.locator(
            "[data-cy='camera-mini-player'] .qtoig07"
        )

    @property
    def camera_mode_in_mini_player(self):
        return self.page.locator(
            "[data-cy='camera-mini-player'] ._1ra3hyj5"
        )

    @property
    def mini_player_timeline(self):
        return self.page.locator(
            "[data-cy='player-timeline-box']"
        )

    @property
    def add_camera_modal(self):
        return self.page.locator(
            "[data-cy='camera-form']"
        )

    @property
    def camera_name_field_in_create_modal(self):
        return self.page.locator(
            "[data-cy='camera-name-input']"
        )

    @property
    def camera_name_field_in_edit_modal(self):
        return self.page.locator(
            "[name='name']"
        )

    @property
    def camera_url_field(self):
        return self.page.locator(
            "[data-cy='camera-url-input']"
        )

    @property
    def video_protocol_dropdown_camera_modal(self):
        return self.page.locator(
            "[data-cy='protocol-toggle-button']"
        )

    @property
    def rtmp_protocol_camera_modal(self):
        return self.page.locator(
            "[data-cy-value='rtmp']"
        )

    @property
    def rtsp_protocol_camera_modal(self):
        return self.page.locator(
            "[data-cy-value='rtsp']"
        )

    @property
    def transport_protocol_dropdown_camera_modal(self):
        return self.page.locator(
            "[data-cy='transport-toggle-button']"
        )

    @property
    def tcp_protocol_camera_modal(self):
        return self.page.locator(
            "[data-cy-value='tcp']"
        )

    @property
    def udp_protocol_camera_modal(self):
        return self.page.locator(
            "[data-cy-value='udp']"
        )

    @property
    def cluster_dropdown_camera_modal(self):
        return self.page.locator(
            "[data-cy='capacity-group-toggle-button']"
        )

    @property
    def clusters_camera_modal(self):
        return self.page.locator(
            "[data-cy='capacity-group-option']"
        )

    @property
    def place_dropdown_camera_modal(self):
        return self.page.locator(
            "[data-cy='camera-form'] [data-cy='place-picker-trigger']"
        )

    @property
    def input_validation_warning_in_camera_modal(self):
        return self.page.locator(
            "[data-cy='input-validation-warning']"
        )

    @property
    def place_name_in_places_modal(self):
        return self.page.locator(
            "[data-cy='place-name']"
        )

    @property
    def place_item_in_places_modal(self):
        return self.page.locator(
            "[data-cy='place-picker-item']"
        )

    @property
    def places_modal_submit_button(self):
        return self.page.locator(
            "[data-cy='place-complex-picker-submit-button']"
        )

    @property
    def new_camera_submit_button(self):
        return self.page.locator(
            "[data-cy='new-camera-submit']"
        )

    @property
    def edit_camera_button(self):
        return self.page.locator(
            "[data-cy='edit-camera-link']"
        )

    @property
    def edit_camera_submit_button(self):
        return self.page.locator(
            "[data-cy='edit-camera-submit']"
        )

    @property
    def close_modal_button(self):
        return self.page.locator(
            "[data-cy='modal-close-button']"
        )

    @property
    def delete_camera_button(self):
        return self.page.locator(
            "[data-cy='destroy-camera-submit']"
        )

    @property
    def confirm_delete_camera_button(self):
        return self.page.locator(
            "[data-cy='confirm-button']"
        )

    @property
    def camera_status_unavailable(self):
        return self.page.locator(
            "[data-cy-value='unavailable']"
        )

    @property
    def place_modal_search_input(self):
        return self.page.locator(
            "[data-cy='place-search-input']"
        )

    def open_camera_create_modal(self):
        self.add_camera_button.click()

    def open_camera_edit_modal(self):
        self.cameras_overlay_items.first.hover()
        self.edit_camera_button.first.click()

    def search_camera(self, name: str):
        self.search_field.fill(name)

    def create_new_camera(self, name: str, url: str):
        self.camera_name_field_in_create_modal.fill(name)
        self.camera_url_field.fill(url)
        self.transport_protocol_dropdown_camera_modal.click()
        self.tcp_protocol_camera_modal.click()
        self.cluster_dropdown_camera_modal.click()
        self.clusters_camera_modal.first.click()
        self.place_dropdown_camera_modal.click()
        self.place_item_in_places_modal.first.click()
        self.places_modal_submit_button.click()
        self.new_camera_submit_button.click()

    def edit_camera(self, name: str, url: str):
        self.camera_name_field_in_edit_modal.fill(name)
        self.camera_url_field.fill(url)
        self.edit_camera_submit_button.click()

    def delete_camera_by_name(self, name: str):
        if self.close_modal_button.is_visible():
            self.close_modal_button.click()
        self.search_camera(name)
        self.open_camera_edit_modal()
        self.delete_camera_button.click()
        self.confirm_delete_camera_button.click()

    def open_mini_player(self):
        self.cameras_overlay_items.first.click()

    def select_place_by_name(self, name: str):
        self.places_modal_button.click()
        self.place_modal_search_input.fill(name)
        self.click_item_by_text(self.place_item_in_places_modal, name)
        self.places_modal_submit_button.click()

    def select_va_by_name(self, name: str):
        self.video_module_dropdown.click()
        self.click_item_by_text(self.video_module_options, name)

    def assert_camera_by_name_not_in_grid(self, name: str):
        expect(
            self.page.locator(f'[data-cy="camera-item"] [title="{name}"]')
        ).not_to_be_visible()

    def assert_value_in_url_field_is_equal(self, url: str):
        expect(self.camera_url_field).to_have_value(url)

    def assert_cameras_title(self):
        expect(self.cameras_title).to_be_visible()

    def assert_groups_dropdown(self):
        expect(self.groups_dropdown).to_be_visible()

    def assert_places_modal_button(self):
        expect(self.places_modal_button).to_be_visible()

    def assert_clusters_dropdown(self):
        expect(self.clusters_dropdown).to_be_visible()

    def assert_video_module_dropdown(self):
        expect(self.video_module_dropdown).to_be_visible()

    def assert_state_camera_dropdown(self):
        expect(self.camera_state_dropdown).to_be_visible()

    def assert_add_tags_button(self):
        expect(self.add_tags_buttons.first).to_be_visible()

    def assert_add_camera_button(self):
        expect(self.add_camera_button).to_be_visible()

    def assert_search_field(self):
        expect(self.search_field).to_be_visible()

    def assert_cameras_grid(self):
        expect(self.camera_items.first).to_be_visible()

    def assert_cameras_pagination(self):
        initial = self.camera_items.count()
        self.scroll_to_bottom(self.page_content)
        self.page.wait_for_timeout(500)
        assert self.camera_items.count() > initial

    def assert_mini_player_open(self):
        expect(self.camera_mini_player).to_be_visible()

    def assert_camera_name_in_mini_player(self):
        expect(self.camera_name_in_mini_player).to_be_visible()

    def assert_camera_mode_in_mini_player(self):
        expect(self.camera_mode_in_mini_player).to_be_visible()

    def assert_add_camera_modal(self):
        expect(self.add_camera_modal).to_be_visible()

    def assert_create_camera_modal_empty_fields_validation(self):
        expected_warnings_count = 4
        self.new_camera_submit_button.click()
        expect(self.input_validation_warning_in_camera_modal).to_have_count(expected_warnings_count)

    def assert_add_camera_modal_fields(self):
        expect(self.add_camera_modal).to_be_visible()
        expect(self.camera_name_field_in_create_modal).to_be_visible()
        expect(self.camera_url_field).to_be_visible()
        expect(self.video_protocol_dropdown_camera_modal).to_be_visible()
        expect(self.transport_protocol_dropdown_camera_modal).to_be_visible()
        expect(self.cluster_dropdown_camera_modal).to_be_visible()
        expect(self.place_dropdown_camera_modal).to_be_visible()
        expect(self.new_camera_submit_button).to_be_visible()

    def assert_filter_panel_is_visible(self):
        self.assert_groups_dropdown()
        self.assert_places_modal_button()
        self.assert_clusters_dropdown()
        self.assert_video_module_dropdown()
        self.assert_state_camera_dropdown()
        self.assert_add_tags_button()
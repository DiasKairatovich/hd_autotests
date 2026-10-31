from __future__ import annotations
from playwright.sync_api import expect, TimeoutError as PWTimeout
from core.ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    PATH = "/dashboard"
    def __init__(self, page, settings):
        super().__init__(page)
        self.URL = settings.ui_base_url + self.PATH

    @property
    def dashboard_content(self):
        return self.page.locator(
            "[data-cy='page-content']"
        )

    @property
    def total_cameras(self):
        return self.page.locator(
            "[data-cy='cameraTotal-grid-item']"
        )

    @property
    def total_events(self):
        return self.page.locator(
            "[data-cy='eventsTotal-grid-item']"
        )

    @property
    def user_menu_button(self):
        return self.page.locator(
            "button[data-cy='toggle-user-menu']:visible"
        )

    @property
    def logout_button(self):
        return self.page.locator(
            "[data-cy='logout']"
        )

    @property
    def dashboard_title(self):
        return self.page.locator(
            "(//*[@role='tab'])[1]"
        )

    @property
    def cameras_total_count(self):
        return self.page.locator(
            "[data-cy='cameras-total-count']"
        )

    @property
    def events_total_count(self):
        return self.page.locator(
            "[data-cy='events-total-count']"
        )

    @property
    def events_priority_chart(self):
        return self.page.locator(
            "[data-cy='events-by-priority-widget'] svg g"
        )

    @property
    def events_type_chart(self):
        return self.page.locator(
            "[data-cy='events-by-type-period-widget'] svg g"
        )

    @property
    def unique_persons_widget(self):
        return self.page.locator(
            "[data-cy='cohort-total-widget']"
        )

    @property
    def recently_events_widget(self):
        return self.page.locator(
            "[data-cy='events-list-widget']"
        )

    @property
    def recently_event(self):
        return self.page.locator(
            "[data-cy='event-hero-link']"
        )

    @property
    def recently_events_error_button(self):
        return self.page.locator(
            "[data-cy='eventsList-grid-item'] .fh22rs1.fh22rs0 button[type='button']"
        )

    def open(self, timeout: int = 30000) -> "DashboardPage":
        super().open(self.URL)
        self.cameras_total_count.wait_for(state='visible')
        self.scroll_to_bottom(self.dashboard_content)
        return self

    def assert_dashboard_page_loaded(self, timeout: int = 20000) -> "DashboardPage":
        expect(self.total_cameras.first).to_be_visible(timeout=timeout)
        expect(self.total_events.first).to_be_visible(timeout=timeout)
        return self

    def _wait_page_stable(self, timeout=30000):
        for sel in ('[data-cy="global-loader"]',
                    '[data-cy="page-loader"]',
                    '#nprogress', '.nprogress'):
            loc = self.page.locator(sel)
            try:
                loc.wait_for(state="hidden", timeout=500)
            except PWTimeout:
                try:
                    loc.wait_for(state="detached", timeout=timeout)
                except PWTimeout:
                    pass

        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except PWTimeout:
            pass

    def user_menu_open(self, timeout=50000) -> "DashboardPage":
        self._wait_page_stable()
        btn = self.user_menu_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.scroll_into_view_if_needed()
        btn.hover()
        btn.click()

    def assert_user_menu_loaded(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.user_menu_button).to_be_visible(timeout=timeout)
        return self

    def assert_logout_button_loaded(self, timeout: int = 20000) -> "DashboardPage":
        expect(self.logout_button.first).to_be_visible(timeout=timeout)
        return self

    def assert_dashboard_title_is_visible(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.dashboard_title).to_be_visible(timeout=timeout)
        return self

    def assert_cameras_total_count(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.cameras_total_count).to_be_visible(timeout=timeout)
        return self

    def assert_events_total_count(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.events_total_count).to_be_visible(timeout=timeout)
        return self

    def assert_events_priority_chart(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.events_priority_chart.first).to_be_visible(timeout=timeout)
        return self

    def assert_events_type_chart(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.events_type_chart.first).to_be_visible(timeout=timeout)
        return self

    def assert_unique_persons_widget(self, timeout: int = 30000) -> "DashboardPage":
        expect(self.unique_persons_widget.first).to_be_visible(timeout=timeout)
        return self

    def assert_recently_events_widget(self, timeout: int = 30000) -> "DashboardPage":
        if self.recently_event.first.is_visible(timeout=timeout):
            return self

        if self.recently_events_error_button.is_visible(timeout=timeout):
            raise AssertionError()

        return self

    def assert_dashboard_widgets_loaded(self) -> "DashboardPage":
        self.assert_cameras_total_count()
        self.assert_events_total_count()
        self.assert_events_priority_chart()
        self.assert_events_type_chart()
        self.assert_unique_persons_widget()
        self.assert_recently_events_widget()
        return self

    def logout(self) -> "DashboardPage":
        self.logout_button.first.click()
        return self
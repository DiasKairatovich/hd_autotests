import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.tms("TC-133")
@pytest.mark.smoke
@pytest.mark.events
def test_events_page_is_opened(auth, events_page):
    with allure.step("Перейти в раздел «События»"):
        events_page.open()

    with allure.step("Проверить наличие панели фильтров"):
        expect(events_page.panel_filter).to_be_visible()

    with allure.step("Проверить вкладки «Фильтры», «Подписка», «Датчики», «Поиск»"):
        expect(events_page.tab_filter).to_be_visible()
        expect(events_page.tab_subscription).to_be_visible()
        expect(events_page.tab_sensor).to_be_visible()
        expect(events_page.tab_search).to_be_visible()

    with allure.step("Проверить наличие всех полей фильтров (дата/время, группа, место, камера, лица, списки)"):
        expect(events_page.group_dropdown).to_be_visible()
        expect(events_page.place_dropdown).to_be_visible()
        expect(events_page.list_dropdown).to_be_visible()
        expect(events_page.camera_dropdown).to_be_visible()
        expect(events_page.event_type_dropdown).to_be_visible()

    with allure.step("Проверить отображение карточек событий на странице"):
        expect(events_page.event_list.or_(events_page.event_list_item.first)).to_be_visible()




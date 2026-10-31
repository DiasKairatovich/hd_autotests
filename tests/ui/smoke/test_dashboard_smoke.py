import allure
import pytest

@pytest.mark.tms("TC-36")
@pytest.mark.smoke
@pytest.mark.dashboard
def test_dashboard_page_loads(auth, dashboard_page):
    with allure.step("Проверить загрузку страницы"):
        dashboard_page.open()
        dashboard_page.assert_dashboard_page_loaded()

    with allure.step("Проверить заголовок"):
        dashboard_page.assert_dashboard_title_is_visible()

    with allure.step("Проверить корректную загрузку всех основных блоков"):
        dashboard_page.assert_dashboard_widgets_loaded()

@pytest.mark.tms("TC-37")
@pytest.mark.smoke
@pytest.mark.dashboard
def test_all_cameras(auth, dashboard_page):
    with allure.step("Найти блок Все камеры"):
        dashboard_page.open()
        dashboard_page.assert_cameras_total_count()
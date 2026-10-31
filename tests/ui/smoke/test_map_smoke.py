import allure
import pytest


@pytest.mark.tms("TC-178")
@pytest.mark.smoke
@pytest.mark.map
def test_elements_is_visible(auth, map_page):
    with allure.step("Открыть раздел “Карта“"):
        map_page.open()

    with allure.step("Проверить наличие основных компонентов"):
        map_page.check_page_elements()

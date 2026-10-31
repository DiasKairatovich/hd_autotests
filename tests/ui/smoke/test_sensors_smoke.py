import allure
import pytest

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data


@pytest.mark.tms("TC-753")
@pytest.mark.smoke
@pytest.mark.sensors
def test_sensors_crud(auth, sensors_page, camera, place, api_client):
    sensor_name = data.sensor_data()['name']
    sensor_name_edited = data.sensor_data()['name']
    place_name = place.json()['name']
    entity_name = None
    with allure.step("Предусловия. Открыта страница Датчики"):
        sensors_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить датчик“"):
            sensors_page.add_sensor_button.click()

        with allure.step("Заполнить необходимые поля и нажать кнопку “Добавить“"):
            sensors_page.sensor_name_field_in_modal.fill(sensor_name)
            sensors_page.sensor_kinds_dropdown.click()
            sensors_page.sensor_kinds_options.first.evaluate("el => el.click()")
            sensors_page.sensor_place_dropdown.click()
            sensors_page.sensor_place_search_field.fill(place_name)
            sensors_page.sensor_place_items.first.click()
            sensors_page.sensor_place_submit_button.click()
            sensors_page.camera_sensor_dropdown.first.evaluate("el => el.click()")
            sensors_page.camera_sensor_options.first.evaluate("el => el.click()")
            sensors_page.add_sensor_submit_button.click()

        with allure.step("Проверить отображение датчика в выдаче с указанными данными"):
            sensors_page.search_sensor_field.fill(sensor_name)
            entity_name = sensor_name
            sensors_page.assert_element_name_is_equal(sensors_page.sensor_cards, sensor_name)

        with allure.step("Открыть модальное окно редактирования и изменить данные датчика, сохранить датчик"):
            sensors_page.edit_sensor_button.click()
            sensors_page.sensor_name_field_in_modal.fill(sensor_name_edited)
            sensors_page.sensor_kinds_dropdown.click()
            sensors_page.sensor_kinds_options.first.evaluate("el => el.click()")
            sensors_page.sensor_place_dropdown.click()
            sensors_page.sensor_place_search_field.fill(place_name)
            sensors_page.sensor_place_items.first.click()
            sensors_page.sensor_place_submit_button.click()
            sensors_page.camera_sensor_dropdown.first.evaluate("el => el.click()")
            sensors_page.camera_sensor_options.first.evaluate("el => el.click()")
            sensors_page.edit_sensor_submit_button.click()
            entity_name = sensor_name_edited

        with allure.step("Проверить отображение датчика в выдаче с указанными данными"):
            sensors_page.search_sensor_field.fill(sensor_name_edited)
            sensors_page.assert_element_name_is_equal(sensors_page.sensor_cards, sensor_name_edited)

        with allure.step("Удалить датчик"):
            sensors_page.delete_sensor_button.click()
            sensors_page.sensor_delete_confirm_button.click()

        with allure.step("Проверить, что удаленный датчик не отображается в выдаче"):
            sensors_page.assert_element_not_present_by_text(sensors_page.sensor_cards, sensor_name_edited)

    except Exception:
        if entity_name is not None:
            with allure.step("Удалить датчик"):
                delete_with_retry_by_name(
                    api_client.search_sensors,
                    api_client.delete_sensor,
                    entity_name
                )

        raise
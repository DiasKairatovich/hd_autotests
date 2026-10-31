import time

import allure
import pytest
from playwright.sync_api import expect

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data


@pytest.mark.tms("TC-57")
@pytest.mark.smoke
@pytest.mark.cameras
def test_cameras_page_loads(auth, cameras_page):
    with allure.step("Перейти в меню Камеры"):
        cameras_page.open()

    with allure.step("Проверить наличие заголовка"):
        cameras_page.assert_cameras_title()

    with allure.step("Проверить отсутствие ошибок загрузки"):
        cameras_page.assert_no_toast_error()

@pytest.mark.tms("TC-58")
@pytest.mark.smoke
@pytest.mark.cameras
def test_cameras_page_elements(auth, cameras_page, cameras_grid):
    with allure.step("Пользователь на странице «Камеры»"):
        cameras_page.open()

    with allure.step("Проверить наличие панели фильтров (состояние, кластер, место, VA, теги)"):
        cameras_page.assert_filter_panel_is_visible()

    with allure.step("Проверить наличие поля поиска и кнопки «Добавить камеру»"):
        cameras_page.assert_add_camera_button()
        cameras_page.assert_search_field()

    with allure.step("Проверить отображение списка/сетки камер, пагинации"):
        cameras_page.assert_cameras_grid()
        cameras_page.assert_cameras_pagination()

@pytest.mark.tms("TC-60")
@pytest.mark.smoke
@pytest.mark.cameras
def test_camera_mini_player(auth, cameras_page, camera):
    with allure.step("На странице «Камеры» кликнуть на любую карточку камеры"):
        cameras_page.open()
        cameras_page.open_mini_player()
        cameras_page.assert_mini_player_open()

    with allure.step("Проверить отображение основной информации (название, статус, таймлайн)"):
        cameras_page.assert_camera_name_in_mini_player()
        cameras_page.assert_camera_mode_in_mini_player()


@pytest.mark.tms("TC-61")
@pytest.mark.smoke
@pytest.mark.cameras
def test_add_camera_modal_is_open(auth, cameras_page):
    with allure.step("Открыть страницу «Камеры». Проверить наличие кнопки Добавить камеру"):
        cameras_page.open()
        cameras_page.assert_add_camera_button()

    with allure.step("Нажать кнопку «Добавить камеру». Проверить открытие модального окна добавления камеры"):
        cameras_page.add_camera_button.click()
        cameras_page.assert_add_camera_modal()

@pytest.mark.tms("TC-64")
@pytest.mark.smoke
@pytest.mark.cameras
def test_filter_by_place(auth, cameras_page, camera, place):
    place_name = place.json()['name']
    with allure.step("Предусловия. Открыта страница Камеры"):
        cameras_page.open()

    with allure.step("Выбрать конкретное место в фильтре мест. Отображаются только камеры этого места"):
        cameras_page.select_place_by_name(place_name)
        cameras_page.scroll_to_bottom(cameras_page.page_content)
        cameras_page.assert_all_texts_in_elements_are_equal(cameras_page.camera_places_in_items, place_name)

    with allure.step("Сбросить фильтр места. Фильтр сброшен"):
        cameras_page.reset_place_filter_button.click()
        expect(cameras_page.reset_place_filter_button).not_to_be_visible()

@pytest.mark.tms("TC-65")
@pytest.mark.smoke
@pytest.mark.cameras
def test_filter_by_va(auth, cameras_page, camera):
    with allure.step("Предусловия. Открыта страница Камеры"):
        cameras_page.open()

    with allure.step("Выбрать фильтр VA (например: «Движение»)"):
        cameras_page.video_module_dropdown.click()
        selected_va = cameras_page.video_module_options.first.inner_text()
        cameras_page.click_item_by_text(cameras_page.video_module_options, selected_va)
        cameras_page.assert_all_texts_in_elements_are_equal(cameras_page.camera_video_modules_in_items.first, selected_va)

    with allure.step("Выключить/сменить VA-фильтр"):
        cameras_page.video_module_dropdown.click()
        selected_va = cameras_page.video_module_options.last.inner_text()
        cameras_page.click_item_by_text(cameras_page.video_module_options, selected_va)
        cameras_page.assert_all_texts_in_elements_are_equal(cameras_page.camera_video_modules_in_items.first, selected_va)

    with allure.step("Сбросить VA-фильтр. Фильтр сброшен"):
        cameras_page.reset_video_module_filter_button.click()
        expect(cameras_page.reset_video_module_filter_button).not_to_be_visible()

@pytest.mark.tms("TC-67")
@pytest.mark.smoke
@pytest.mark.cameras
def test_search_camera_by_name(auth, cameras_page, camera):
    camera = camera.json()
    with allure.step("Предусловия. Открыт раздел Камеры. Создана тестовая камера"):
        cameras_page.open()

    with allure.step("Ввести полное название камеры в поле поиска и выполнить поиск. Отображается только камера с точным названием"):
        cameras_page.search_camera(camera['name'])
        cameras_page.assert_all_texts_in_elements_are_equal(cameras_page.camera_names_in_items, camera['name'])

    with allure.step("Ввести часть названия (частичный матч). Показаны все камеры, содержащие введённую подстроку"):
        cameras_page.search_camera(camera['name'][:4])
        cameras_page.assert_all_texts_in_elements_contain(cameras_page.camera_names_in_items, camera['name'][:4])

    with allure.step("Очистить поле поиска"):
        cameras_page.search_clear_button.click()
        expect(cameras_page.search_clear_button).not_to_be_visible()

@pytest.mark.tms("TC-68")
@pytest.mark.smoke
@pytest.mark.cameras
def test_pagination_cameras(auth, cameras_page, cameras_grid):
    with allure.step("Предусловия. Открыта страница Камеры"):
        cameras_page.open()

    with allure.step("Пролистать список до конца (infinite scroll)"):
        cameras_page.assert_cameras_pagination()

@pytest.mark.tms("TC-72")
@pytest.mark.smoke
@pytest.mark.cameras
def test_camera_add_form_opens(auth, cameras_page):
    with allure.step("Предусловия. Открыть страницу Камеры"):
        cameras_page.open()

    with allure.step("На странице «Камеры» нажать «Добавить камеру»"):
        cameras_page.add_camera_button.click()

    with allure.step("Проверить наличие обязательных полей (название, поток, место и т.д.)"):
        cameras_page.assert_add_camera_modal_fields()

    with allure.step("Проверить валидацию полей при пустых значениях (нажать «Сохранить»)"):
        cameras_page.assert_create_camera_modal_empty_fields_validation()

@pytest.mark.tms("TC-73")
@pytest.mark.smoke
@pytest.mark.cameras
def test_create_new_camera(auth, cameras_page, place, api_client):
    camera = data.camera_data()
    entity_name = None

    try:
        with allure.step("Открыть страницу и нажать на кнопку Добавить камеру"):
            cameras_page.open()
            cameras_page.add_camera_button.click()

        with allure.step("Заполнить форму валидными данными и нажать «Сохранить», проверить появление подтверждения"):
            cameras_page.create_new_camera(camera['name'], camera['source']['url'])
            entity_name = camera['name']
            cameras_page.assert_toast_success()

        with allure.step("Проверить появление новой камеры в списке (поиск/фильтр по названию)"):
            cameras_page.search_camera(camera['name'])
            cameras_page.assert_element_name_is_equal(cameras_page.camera_items, camera['name'])

        with allure.step("Открыть карточку новой камеры и проверить основные поля"):
            cameras_page.open_camera_edit_modal()
            cameras_page.assert_field_value_is_equal(cameras_page.camera_name_field_in_edit_modal, camera['name'])
            cameras_page.assert_field_value_is_equal(cameras_page.camera_url_field, camera['source']['url'])

        with allure.step("Постусловия. Удалить созданную ранее тестовую камеру"):
            cameras_page.delete_camera_by_name(camera['name'])
            cameras_page.assert_element_not_present_by_text(cameras_page.camera_items, camera['name'])
    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_cameras,
                api_client.delete_camera,
                entity_name
            )
        raise

@pytest.mark.tms("TC-74")
@pytest.mark.smoke
@pytest.mark.cameras
def test_edit_camera(auth, cameras_page, camera, api_client):
    camera = camera.json()
    edited_camera = data.camera_data()
    entity_name = None

    try:
        with allure.step("Предусловия. Добавить тестовую камеру"):
            cameras_page.open()
            entity_name = camera['name']

        with allure.step("Открыть страницу Камеры, в списке нажать «Редактировать» на карточке камеры"):
            cameras_page.search_camera(camera['name'])
            cameras_page.open_camera_edit_modal()

        with allure.step("Изменить одно или несколько полей и сохранить"):
            cameras_page.edit_camera(edited_camera['name'], edited_camera['source']['url'])
            entity_name = edited_camera['name']
            cameras_page.assert_toast_success()
            cameras_page.close_modal_button.click()

        with allure.step("Проверить, что изменения видны в карточке и списке"):
            cameras_page.search_camera(edited_camera['name'])
            cameras_page.assert_element_name_is_equal(cameras_page.camera_items, edited_camera['name'])
            time.sleep(2) # добавить нормальное ожидание
            cameras_page.open_camera_edit_modal()
            cameras_page.assert_value_in_url_field_is_equal(edited_camera['source']['url'])

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_cameras,
                api_client.delete_camera,
                entity_name
            )
        raise
@pytest.mark.tms("TC-75")
@pytest.mark.smoke
@pytest.mark.cameras
def test_delete_camera(auth, cameras_page, camera, api_client):
    entity_name = None
    try:
        with allure.step("Предусловия. Добавить тестовую камеру"):
            cameras_page.open()

        with allure.step("Открыть модальное окно редактирования камеры. Нажать «Удалить» на выбранной камере"):
            cameras_page.search_camera(camera.json()['name'])
            entity_name = camera.json()['name']
            cameras_page.open_camera_edit_modal()
            cameras_page.delete_camera_button.click()

        with allure.step("Подтвердить удаление"):
            cameras_page.confirm_delete_camera_button.click()
            cameras_page.assert_toast_success()

        with allure.step("Проверить, что камера исчезла из списка и поиск не находит её"):
            cameras_page.search_camera(camera.json()['name'])
            cameras_page.assert_camera_by_name_not_in_grid(camera.json()['name'])
    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_cameras,
                api_client.delete_camera,
                entity_name
            )
        raise
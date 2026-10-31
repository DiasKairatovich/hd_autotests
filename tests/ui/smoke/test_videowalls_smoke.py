import allure
import pytest
from playwright.sync_api import expect

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data
from tests.ui.conftest import cameras_page


@pytest.mark.tms("TC-103")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_videowalls_page_loads(auth, videowalls_page):
    with allure.step("Предусловия. Открыть страницу «Видеостены»"):
        videowalls_page.open()

    with allure.step("Проверить наличие заголовка «Видеостены»"):
        expect(videowalls_page.videowalls_title).to_be_visible()

@pytest.mark.tms("TC-104")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_add_videowall_button_is_visible(auth, videowalls_page):
    with allure.step("Предусловия. Открыть страницу «Видеостены»"):
        videowalls_page.open()

    with allure.step("Проверить наличие кнопки “Добавить видеостену”"):
        expect(videowalls_page.add_videowall_button).to_be_visible()

    with allure.step("Проверить что кнопка кликабельна"):
        expect(videowalls_page.add_videowall_button).to_be_enabled()

@pytest.mark.tms("TC-105")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_videowall_create_modal_opens(auth, videowalls_page):
    with allure.step("Предусловия. Открыть страницу «Видеостены»"):
        videowalls_page.open()

    with allure.step("Нажать кнопку “Добавить видеостену”. Проверить открытие формы"):
        videowalls_page.add_videowall_button.click()
        expect(videowalls_page.create_videowall_modal).to_be_visible()

    with allure.step("Проверить наличие полей формы"):
        expect(videowalls_page.videowall_name_field_in_create_modal).to_be_visible()
        expect(videowalls_page.videowall_user_field_in_create_modal).to_be_visible()

@pytest.mark.tms("TC-106")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_videowalls_grid_is_loaded(auth, videowall, videowalls_page):
    with allure.step("Предусловия. Открыть страницу «Видеостены»"):
        videowalls_page.open()

    with allure.step("Проверить отображение списка видеостен"):
        expect(videowalls_page.videowall_cards.first).to_be_visible()

    with allure.step("Проверить отображение названий видеостен"):
        expect(videowalls_page.videowall_names.first).to_be_visible()

@pytest.mark.tms("TC-107")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_videowall_is_opened(auth, videowall, videowalls_page, cameras_page):
    with allure.step("Предусловия. Открыта страница Видеостены"):
        videowalls_page.open()

    with allure.step("Нажать на существующую видеостену"):
        videowalls_page.search_videowall_by_name(videowall)
        videowalls_page.videowall_cards.first.click()

    with allure.step("Проверить наличие сетки камер"):
        expect(videowalls_page.camera_cards_in_videowall.first).to_be_visible()

    with allure.step("Проверить отсутствие ошибок трансляции"):
        expect(cameras_page.retry_stream_button.first).not_to_be_visible()

@pytest.mark.tms("TC-108")
@pytest.mark.smoke
@pytest.mark.videowalls
@pytest.mark.skip("Bug: EYE-5663")
def test_edit_videowall_button_is_visible(auth, videowalls_page):
    with allure.step("Предусловия. Открыта видеостена"):
        videowalls_page.open()
        videowalls_page.videowall_cards.first.click()

    with allure.step("Проверить наличие кнопки “Редактировать”"):
        expect(videowalls_page.edit_videowall_button).to_be_visible()

    with allure.step("Проверить что кнопка кликабельна"):
        expect(videowalls_page.edit_videowall_button).to_be_enabled()

@pytest.mark.tms("TC-117")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_create_videowall(auth, videowalls_page, settings, api_client):
    videowall_name = data.videowall_data()["name"]
    user_name = settings.username
    entity_name = None

    try:
        with allure.step("Нажать «+ Добавить видеостену»"):
            videowalls_page.open()
            videowalls_page.add_videowall_button.click()
            expect(videowalls_page.create_videowall_modal).to_be_visible()

        with allure.step("Заполнить поле Название"):
            videowalls_page.videowall_name_field_in_create_modal.fill(videowall_name)
            expect(videowalls_page.videowall_name_field_in_create_modal).not_to_be_empty()

        with allure.step("Выбрать пользователей"):
            videowalls_page.videowall_user_field_in_create_modal.click()
            videowalls_page.videowall_user_field_in_create_modal.fill(user_name)
            videowalls_page.user_options.first.evaluate("el => el.click()")

        with allure.step("Выбрать тип сетки x4"):
            videowalls_page.videowall_grid_in_create_modal_type2.click()

        with allure.step("Добавить 4 камеры"):
            videowalls_page.next_button_in_create_modal.click()
            videowalls_page.add_cameras_in_create_grid()

        with allure.step("Нажать “Сохранить”"):
            videowalls_page.save_videowall_button.click()
            entity_name = videowall_name

        with allure.step("Проверить создание видеостены"):
            videowalls_page.assert_element_name_is_equal(videowalls_page.videowall_cards, videowall_name)

        with allure.step("Удалить созданную ранее видеостену"):
            videowalls_page.delete_videowall_by_name(videowall_name)

        with allure.step("Проверить, что удаленная видеостена не отображается в выдаче"):
            videowalls_page.assert_element_not_present_by_text(videowalls_page.videowall_cards, videowall_name)

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_videowalls,
                api_client.delete_videowall,
                entity_name
            )
        raise

@pytest.mark.tms("TC-127")
@pytest.mark.smoke
@pytest.mark.videowalls
def test_edit_videowall(auth, videowalls_page, settings, api_client):
    videowall_name = data.videowall_data()["name"]
    videowall_name_edited = data.videowall_data()["name"]
    user_name = settings.username
    entity_name = None

    try:
        with allure.step("Предусловия. Есть созданная видеостена"):
            videowalls_page.open()
            entity_name = videowall_name
            videowalls_page.create_new_videowall(videowall_name, user_name)

        with allure.step("Найти созданную видеостену"):
            videowalls_page.search_videowall_by_name(videowall_name)
            videowalls_page.assert_element_name_is_equal(videowalls_page.videowall_cards, videowall_name)

        with allure.step("Нажать редактировать"):
            videowalls_page.videowall_menu_button.first.click()
            videowalls_page.edit_button_in_videowall_menu.first.click()

        with allure.step("Изменить название"):
            videowalls_page.videowall_name_field_in_edit_modal.fill(videowall_name_edited)

        with allure.step("Сохранить изменения"):
            videowalls_page.videowall_submit_button_in_edit_modal.click()
            entity_name = videowall_name_edited
            videowalls_page.search_videowall_by_name(videowall_name_edited)
            videowalls_page.assert_element_name_is_equal(videowalls_page.videowall_cards, videowall_name_edited)

        with allure.step("Постусловия. Удалить созданную видеостену"):
            videowalls_page.delete_videowall_by_name(videowall_name_edited)

        with allure.step("Проверить, что удаленная видеостена не отображается в выдаче"):
            videowalls_page.assert_element_not_present_by_text(videowalls_page.videowall_cards, videowall_name_edited)

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_videowalls,
                api_client.delete_videowall,
                entity_name
            )
        raise
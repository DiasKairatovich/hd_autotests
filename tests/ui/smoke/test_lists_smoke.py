import allure
import pytest

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data


@pytest.mark.tms("TC-748")
@pytest.mark.smoke
@pytest.mark.lists
def test_face_lists_crud(auth, lists_page, api_client):
    list_name = data.list_data()["name"]
    list_name_edited = data.list_data()["name"]
    entity_name = None
    with allure.step("Предусловия. Открыта страница Списки"):
        lists_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить список“"):
            lists_page.add_list_button.click()

        with allure.step("Заполнить поле “Название“ и нажать на кнопку “Сохранить“"):
            lists_page.name_field_in_modal.fill(list_name)
            lists_page.submit_button_in_modal.click()

        with allure.step("Проверить создание списка"):
            lists_page.search_face_lists.fill(list_name)
            entity_name = list_name
            lists_page.assert_element_name_is_equal(lists_page.face_list_cards, list_name)

        with allure.step("Открыть меню карточки списка нажатием на три точки, открыть модальное окно редактирования. Изменить название. Сохранить список"):
            lists_page.face_list_menu_button.hover()
            lists_page.face_list_menu_button.click()
            lists_page.edit_face_list_button.click()
            lists_page.name_field_in_modal.fill(list_name_edited)
            lists_page.submit_button_in_modal.click()
            entity_name = list_name_edited

        with allure.step("Проверить, что название списка изменилось"):
            lists_page.search_face_lists.fill(list_name_edited)
            lists_page.assert_element_name_is_equal(lists_page.face_list_cards, list_name_edited)

        with allure.step("Открыть меню карточки списка нажатием на три точки, открыть модальное окно удаления. Подтвердить удаление"):
            lists_page.face_list_menu_button.hover()
            lists_page.face_list_menu_button.click()
            lists_page.delete_face_list_button.click()
            lists_page.confirm_delete_list_button.click()

        with allure.step("Проверить, что удаленный список не отображается в выдаче"):
            lists_page.assert_element_not_present_by_text(lists_page.face_list_cards, list_name_edited)

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_facelists,
                api_client.delete_facelist,
                entity_name
            )
        raise

@pytest.mark.tms("TC-749")
@pytest.mark.smoke
@pytest.mark.lists
def test_plate_lists_crud(auth, lists_page, api_client):
    list_name = data.list_data()["name"]
    list_name_edited = data.list_data()["name"]
    entity_name = None
    with allure.step("Предусловия. Открыта страница Списки на табе Автономера"):
        lists_page.open()
        lists_page.tab_plates.click()

    try:
        with allure.step("Нажать на кнопку “Добавить список“"):
            lists_page.add_list_button.click()

        with allure.step("Заполнить поле “Название“ и нажать на кнопку “Сохранить“"):
            lists_page.name_field_in_modal.fill(list_name)
            lists_page.submit_button_in_modal.click()
            entity_name = list_name

        with allure.step("Проверить создание списка"):
            lists_page.search_plate_lists.fill(list_name)
            lists_page.assert_element_name_is_equal(lists_page.plate_list_cards, list_name)

        with allure.step("Открыть меню карточки списка нажатием на три точки, открыть модальное окно редактирования. Изменить название. Сохранить список"):
            lists_page.plate_list_menu_button.hover()
            lists_page.plate_list_menu_button.click()
            lists_page.edit_plate_list_button.click()
            lists_page.name_field_in_modal.fill(list_name_edited)
            lists_page.submit_button_in_modal.click()
            entity_name = list_name_edited

        with allure.step("Проверить, что название списка изменилось"):
            lists_page.search_plate_lists.fill(list_name_edited)
            lists_page.assert_element_name_is_equal(lists_page.plate_list_cards, list_name_edited)

        with allure.step("Открыть меню карточки списка нажатием на три точки, открыть модальное окно удаления. Подтвердить удаление"):
            lists_page.plate_list_menu_button.hover()
            lists_page.plate_list_menu_button.click()
            lists_page.delete_plate_list_button.click()
            lists_page.confirm_delete_list_button.click()

        with allure.step("Проверить, что удаленный список не отображается в выдаче"):
            lists_page.assert_element_not_present_by_text(lists_page.plate_list_cards, list_name_edited)

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_platelists,
                api_client.delete_platelist,
                entity_name
            )
        raise
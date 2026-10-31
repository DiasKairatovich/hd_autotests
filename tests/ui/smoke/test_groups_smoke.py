import allure
import pytest
from playwright.sync_api import expect

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data

@pytest.mark.tms("TC-739")
@pytest.mark.smoke
@pytest.mark.groups
def test_groups_crud(auth, groups_page, api_client):
    group_name = data.group_data()['name']
    group_name_edited = data.group_data()['name']
    entity_name = None
    with allure.step("Пользователь авторизирован. Открыт раздел “Группы“"):
        groups_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить группу“"):
            groups_page.add_group_button.click()

        with allure.step("Заполнить поле “Название“ и нажать “Добавить группу“"):
            groups_page.name_field_in_create_modal.fill(group_name)
            groups_page.submit_button_in_create_modal.click()
            entity_name = group_name

        with allure.step("Проверить создание группы"):
            groups_page.search_field.fill(group_name)
            groups_page.assert_element_name_is_equal(groups_page.group_cards, group_name)

        with allure.step("Открыть модалку редактирования и изменить название созданной группы"):
            groups_page.edit_group_button.click()
            groups_page.name_field_in_edit_modal.fill(group_name_edited)
            groups_page.submit_button_in_edit_modal.click()
            expect(groups_page.title_in_edit_modal).to_have_text(group_name_edited)
            entity_name = group_name_edited

        with allure.step("Вернуться на страницу групп, проверить наличие измененной группы"):
            groups_page.open()
            groups_page.search_field.fill(group_name_edited)
            groups_page.assert_element_name_is_equal(groups_page.group_cards, group_name_edited)

        with allure.step("Удалить созданную ранее группу"):
            groups_page.delete_group_button.click()
            groups_page.confirm_delete_button.click()

        with allure.step("Проверить, что удаленная группа не отображается в выдаче"):
            groups_page.assert_element_not_present_by_text(groups_page.group_cards, group_name_edited)

    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_groups,
                api_client.delete_group,
                entity_name
            )
        raise
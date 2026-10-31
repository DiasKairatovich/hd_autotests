import allure
import pytest

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data


@pytest.mark.tms("TC-752")
@pytest.mark.smoke
@pytest.mark.users
def test_users_crud(auth, users_page, group, api_client):
    test_user = data.user_data()
    test_user_edited = data.user_data()
    entity_name = None
    with allure.step("Предусловия. Открыть страницу Пользователи"):
        users_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить пользователя“"):
            users_page.add_user_button.click()

        with allure.step("Заполнить необходимые поля и нажать кнопку “Добавить“"):
            users_page.user_name_input_field.fill(test_user['name'])
            users_page.user_last_name_input_field.fill(test_user['last_name'])
            users_page.user_email_input_field.fill(test_user['email'])
            users_page.generate_password_button.click()
            users_page.user_role_dropdown.click()
            selected_role = users_page.user_role_options.last.inner_text()
            users_page.click_item_by_text(users_page.user_role_options, selected_role)
            users_page.user_groups_dropdown.click()
            users_page.user_group_options.first.click()
            users_page.add_user_submit_button.click()
            entity_name = test_user['name']

        with allure.step("Проверить, что пользователь был создан с указанными данными"):
            users_page.search_input_field.fill(test_user['name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user['email'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user['name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user['last_name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, selected_role)

        with allure.step("Открыть модальное окно редактирования и изменить имя пользователя, роль и тд"):
            users_page.edit_user_button.click()
            users_page.user_name_input_field.fill(test_user_edited['name'])
            users_page.user_last_name_input_field.fill(test_user_edited['last_name'])
            users_page.user_email_input_field.fill(test_user_edited['email'])
            users_page.generate_password_button.click()
            users_page.user_role_dropdown.click()
            selected_role = users_page.user_role_options.first.inner_text()
            users_page.click_item_by_text(users_page.user_role_options, selected_role)
            users_page.user_groups_dropdown.click()
            users_page.user_group_options.last.click()
            users_page.edit_user_submit_button.click()
            entity_name = test_user_edited['name']

        with allure.step("Проверить, что пользователь был изменён с указанными данными"):
            users_page.search_input_field.fill(test_user_edited['name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user_edited['email'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user_edited['name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, test_user_edited['last_name'])
            users_page.assert_element_name_is_equal(users_page.user_cards, selected_role)

        with allure.step("Удалить пользователя"):
            users_page.delete_user_button.click()
            users_page.delete_user_confirm_button.click()

        with allure.step("Проверить, что удаленный пользователь не отображается в выдаче"):
            users_page.assert_element_not_present_by_text(users_page.user_cards, test_user_edited['name'])
    except Exception:
        if entity_name is not None:
            delete_with_retry_by_name(
                api_client.search_users,
                api_client.delete_user,
                entity_name
            )
        raise
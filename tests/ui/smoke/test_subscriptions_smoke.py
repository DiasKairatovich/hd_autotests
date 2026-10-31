import allure
import pytest

from tests.ui import data
from tests.ui.api_cleanup import delete_entity_by_name


@pytest.mark.tms("TC-754")
@pytest.mark.smoke
@pytest.mark.subscriptions
def test_subscriptions_crud(auth, subscriptions_page, camera, api_client):
    subscription_name = data.subscription_data()['name']
    subscription_name_edited = data.subscription_data()['name']
    entity_name = None
    with allure.step("Предусловия. Открыть страницу подписок"):
        subscriptions_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить подписку“"):
            subscriptions_page.add_subscription_button.click()

        with allure.step("Заполнить необходимые поля и нажать кнопку сохранить"):
            subscriptions_page.subscription_name_field.fill(subscription_name)
            subscriptions_page.subscription_camera_dropdown.click()
            subscriptions_page.subscription_camera_options.first.evaluate("el => el.click()")
            subscriptions_page.subscription_save_confirm_button.click()
            entity_name = subscription_name

        with allure.step("Проверить создание подписки с указанным именем"):
            subscriptions_page.assert_element_name_is_equal(subscriptions_page.subscription_items, subscription_name)

        with allure.step("Открыть модальное окно редактирования и изменить название, сохранить подписку"):
            subscriptions_page.select_element_by_text(subscriptions_page.subscription_items, subscription_name
                                                      ).locator(subscriptions_page.edit_subscription_button).click()
            subscriptions_page.subscription_name_field.fill(subscription_name_edited)
            subscriptions_page.subscription_save_confirm_button.click()
            entity_name = subscription_name_edited

        with allure.step("Проверить сохранение подписки с указанным именем"):
            subscriptions_page.assert_element_name_is_equal(subscriptions_page.subscription_items, subscription_name_edited)

        with allure.step("Удалить подписку"):
            subscriptions_page.select_element_by_text(subscriptions_page.subscription_items, subscription_name_edited
                                                      ).locator(subscriptions_page.delete_subscription_button).click()
            subscriptions_page.subscription_delete_confirm_button.click()

        with allure.step("Проверить, что удаленная подписка не отображается в выдаче"):
            subscriptions_page.assert_element_not_present_by_text(subscriptions_page.subscription_items, subscription_name_edited)

    except BaseException:
        if entity_name is not None:
            delete_entity_by_name(
                api_client.get_subscriptions,
                "subscriptions",
                api_client.delete_subscription,
                entity_name,
            )
        raise

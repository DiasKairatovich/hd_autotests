import allure
import pytest

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data


@pytest.mark.tms("TC-756")
@pytest.mark.smoke
@pytest.mark.webhooks
def test_webhooks_crud(auth, webhooks_page, subscription, api_client):
    webhook = data.webhook_data()
    webhook_name = webhook['name']
    webhook_name_edited = data.webhook_data()['name']
    webhook_url = webhook['url']
    subscription_name = subscription.json()['name']
    entity_name = None

    with allure.step("Предусловия. Открыть страницу Вебхуки"):
        webhooks_page.open()

    try:
        with allure.step("Нажать кнопку “Добавить вебхук“"):
            webhooks_page.add_webhook_button.click()

        with allure.step("Заполнить необходимые поля и нажать “Сохранить“"):
            webhooks_page.webhook_name_field_in_modal.fill(webhook_name)
            webhooks_page.webhook_url_field_in_modal.fill(webhook_url)
            webhooks_page.webhook_subscription_dropdown_in_modal.click()
            webhooks_page.select_element_by_text(webhooks_page.webhook_subscription_option_in_dropdown, subscription_name).click()
            webhooks_page.save_webhook_button.click()
            entity_name = webhook_name

        with allure.step("Проверить создание вебхука с указанным названием"):
            webhooks_page.assert_element_name_is_equal(webhooks_page.webhook_cards, webhook_name)

        with allure.step("Нажать на кнопку редактирования добавленного ранее вебхука, "
                          "изменить название и нажать “Сохранить“"):
            webhooks_page.select_element_by_text(webhooks_page.webhook_cards, webhook_name
                                                 ).locator(webhooks_page.edit_button).evaluate("el => el.click()")
            webhooks_page.webhook_name_field_in_modal.fill(webhook_name_edited)
            webhooks_page.webhook_url_field_in_modal.fill(webhook_url)
            webhooks_page.webhook_subscription_dropdown_in_modal.click()
            webhooks_page.select_element_by_text(webhooks_page.webhook_subscription_option_in_dropdown, subscription_name).click()
            webhooks_page.save_webhook_button.click()
            entity_name = webhook_name_edited

        with allure.step("Проверить изменненный вебхук с указанным названием"):
            webhooks_page.assert_element_name_is_equal(webhooks_page.webhook_cards, webhook_name_edited)

        with allure.step("Удалить созданный ранее вебхук"):
            webhooks_page.open()
            webhooks_page.select_element_by_text(webhooks_page.webhook_cards, webhook_name_edited
                                                 ).locator(webhooks_page.delete_button).click()
            webhooks_page.confirm_delete_button.click()

        with allure.step("Проверить, что удаленный вебхук не отображается"):
            webhooks_page.assert_element_not_present_by_text(webhooks_page.webhook_cards, webhook_name_edited)

    except Exception:
        if entity_name is not None:
            with allure.step("Удалить созданный ранее вебхук"):
                delete_with_retry_by_name(
                    api_client.search_webhooks,
                    api_client.delete_webhook,
                    entity_name
                )

        raise

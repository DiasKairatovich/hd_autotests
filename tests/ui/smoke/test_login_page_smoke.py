import allure
import pytest
from playwright.sync_api import expect


@pytest.mark.tms("TC-11")
@pytest.mark.smoke
@pytest.mark.login
def test_login_page_is_opened(login_page):
    with allure.step("Открыть URL страницы авторизации (например /login)"):
        login_page.open()

    with allure.step("Проверить отсутствие ошибок загрузки в UI"):
        expect(login_page.toast_error).not_to_be_visible()

    with allure.step("Проверить наличие основных элементов страницы"):
        expect(login_page.logo).to_be_visible()
        expect(login_page.email).to_be_visible()
        expect(login_page.password).to_be_visible()
        expect(login_page.submit).to_be_visible()

@pytest.mark.tms("TC-12")
@pytest.mark.smoke
@pytest.mark.login
def test_credentials_fields_is_visible(login_page):
    with allure.step("Открыть URL страницы авторизации (например /login)"):
        login_page.open()

    with allure.step("Проверить наличие поля Логин"):
        expect(login_page.email).to_be_visible()

    with allure.step("Проверить наличие поля Пароль"):
        expect(login_page.password).to_be_visible()

    with allure.step("Проверить наличие кнопки Войти"):
        expect(login_page.submit).to_be_visible()

@pytest.mark.tms("TC-13")
@pytest.mark.smoke
@pytest.mark.login
def test_successful_login(login_page):
    with allure.step("Открыть URL страницы авторизации (например /login)"):
        login_page.open()

    with allure.step("Ввести валидные логин и пароль"):
        login_page.fill_credentials()
        expect(login_page.email).not_to_have_value("")
        expect(login_page.password).not_to_have_value("")

    with allure.step("Нажать кнопку Войти"):
        login_page.submit.click()

    with allure.step("Проверить редирект"):
        expect(login_page.sidebar).to_be_visible()

@pytest.mark.tms("TC-14")
@pytest.mark.smoke
@pytest.mark.login
def test_logout(auth, login_page):
    with allure.step("Находясь в системе, открыть меню пользователя"):
        login_page.user_menu.click()
        expect(login_page.logout_button).to_be_visible()

    with allure.step("Нажать “Выйти”"):
        login_page.logout_button.click()

    with allure.step("Проверить редирект"):
        expect(login_page.page).to_have_url(login_page.URL)

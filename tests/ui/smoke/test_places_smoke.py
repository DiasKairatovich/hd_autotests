import allure
import pytest
from playwright.sync_api import expect

from core.helpers.cleanup import delete_with_retry_by_name
from tests.ui import data
from tests.ui.api_cleanup import delete_entity_by_name


@pytest.mark.tms("TC-157")
@pytest.mark.smoke
@pytest.mark.places
def test_places_page_loads(auth, places_page):
    with allure.step("Предусловия. Открыта страница Места"):
        places_page.open()

    with allure.step("Проверить основные элементы страницы"):
        expect(places_page.places_title).to_be_visible()
        expect(places_page.add_place_button).to_be_visible()
        expect(places_page.place_cards.first).to_be_visible()
        expect(places_page.tab_places).to_be_visible()
        expect(places_page.tab_categories).to_be_visible()
        expect(places_page.tab_kinds).to_be_visible()

    with allure.step("Перейти между вкладками “Места“, “Категории“ и “Типы“. Проверить, что переход происходит"):
        places_page.tab_categories.click()
        expect(places_page.add_category_button).to_be_visible()
        places_page.tab_kinds.click()
        expect(places_page.add_kind_button).to_be_visible()

@pytest.mark.tms("TC-158")
@pytest.mark.smoke
@pytest.mark.places
def test_places_crud(auth, places_page, group, api_client):
    place_name = data.place_data()['name']
    place_name_edited = data.place_data()["name"]
    entity_name = None
    with allure.step("Предусловия. Открыта страница Места"):
        places_page.open()

    try:
        with allure.step("Нажать на кнопку “Добавить место“"):
            places_page.add_place_button.click()

        with allure.step("Заполнить поля “Название“ и “Группа“ и нажать “Сохранить“"):
            places_page.place_name_in_create_modal.fill(place_name)
            places_page.place_group_in_create_modal.click()
            places_page.group_options.first.evaluate("el => el.click()")
            places_page.submit_button_in_create_modal.click()

        with allure.step("Проверить отображение добавленного места в списке мест"):
            places_page.search_place_field.fill(place_name)
            entity_name = place_name
            places_page.assert_element_name_is_equal(places_page.place_cards, place_name)

        with allure.step("Нажать на три точки справа от названия места, в выпадающем меню выбрать пункт “Редактировать“"):
            places_page.place_menu_button.first.click()
            places_page.edit_place_button.click()

        with allure.step("Изменить значения в полях “Название“ и “Группа“ и нажать “Сохранить“"):
            places_page.place_name_in_create_modal.fill(place_name_edited)
            places_page.place_name_in_create_modal.click()
            places_page.place_group_in_create_modal.click()
            places_page.group_reset_button_in_modal.first.click()
            places_page.group_options.last.evaluate("el => el.click()")
            places_page.submit_button_in_edit_modal.click()
            entity_name = place_name_edited

        with allure.step("Проверить отображение добавленного места в списке мест"):
            places_page.search_place_field.fill(place_name_edited)
            places_page.assert_element_name_is_equal(places_page.place_cards, place_name_edited)

        with allure.step("Нажать на три точки справа от названия места, в выпадающем меню выбрать пункт “Удалить“"):
            places_page.place_menu_button.first.click()
            places_page.delete_place_button.click()

        with allure.step("Нажать на кнопку “Подтвердить“"):
            places_page.confirm_delete_button.first.click(force=True)

        with allure.step("Проверить, что удаленное место не отображается в выдаче"):
            places_page.assert_element_not_present_by_text(places_page.place_cards, place_name_edited)

    except Exception:
        if entity_name is not None:
            with allure.step("Удалить место"):
                delete_with_retry_by_name(
                    api_client.search_places,
                    api_client.delete_place,
                    entity_name
                )
        raise

@pytest.mark.tms("TC-159")
@pytest.mark.smoke
@pytest.mark.places
def test_placecategories_crud(auth, places_page, api_client):
    category_name = data.category_data()["name"]
    category_name_edited = data.category_data()["name"]
    entity_name = None
    with allure.step("Предусловия. Открыта страница Места"):
        places_page.open()

    with allure.step("Перейти во вкладку “Категории“"):
        places_page.tab_categories.click()

    try:
        with allure.step("Нажать на кнопку “Добавить категорию“"):
            places_page.add_category_button.click()

        with allure.step("Ввести название и нажать кнопку “Добавить“"):
            places_page.category_name_field_in_modal.fill(category_name)
            places_page.submit_button_in_category_create_modal.click()

        with allure.step("Проверить отображение добавленной категории в списке"):
            places_page.search_categories_field.fill(category_name)
            entity_name = category_name
            places_page.assert_element_name_is_equal(places_page.category_cards, category_name)

        with allure.step("Нажать на три точки справа от названия категории, в выпадающем меню выбрать пункт “Переименовать“"):
            places_page.category_menu_button.first.click()
            places_page.edit_category_button.click()

        with allure.step("Изменить название и сохранить категорию"):
            places_page.category_name_field_in_modal.fill(category_name_edited)
            places_page.submit_button_in_category_edit_modal.click()
            entity_name = category_name_edited

        with allure.step("Проверить отображение измененной категории в списке"):
            places_page.category_search_clear_button.click()
            places_page.search_categories_field.fill(category_name_edited)
            places_page.assert_element_name_is_equal(places_page.category_cards, category_name_edited)

        with allure.step("Нажать на три точки справа от названия категории, в выпадающем меню выбрать пункт “Удалить“"):
            places_page.category_menu_button.first.click()
            places_page.delete_category_button.click()

        with allure.step("Нажать на кнопку “Подтвердить“"):
            places_page.confirm_delete_button.first.click(force=True)

        with allure.step("Проверить, что удаленная категория не отображается в выдаче"):
            places_page.assert_element_not_present_by_text(places_page.category_cards, category_name_edited)

    except BaseException:
        if entity_name is not None:
            # Браузером не чистим: если упало UI, то и чистка им же.
            delete_entity_by_name(
                api_client.get_placecategories,
                "placecategories",
                api_client.delete_placecategory,
                entity_name,
            )
        raise

@pytest.mark.tms("TC-160")
@pytest.mark.smoke
@pytest.mark.places
def test_placekinds_crud(auth, places_page, api_client):
    kind_name = data.kind_data()["name"]
    kind_name_edited = data.kind_data()["name"]
    entity_name = None
    with allure.step("Предусловия. Открыта страница Места"):
        places_page.open()

    try:
        with allure.step("Перейти во вкладку “Типы“ и нажать на кнопку “Добавить тип“"):
            places_page.tab_kinds.click()
            places_page.add_kind_button.click()

        with allure.step("Ввести название и выбрать тип в дропдауне. Нажать кнопку “Добавить“"):
            places_page.kind_name_field_in_modal.fill(kind_name)
            places_page.kinds_dropdown_in_modal.click()
            places_page.kinds_options_in_dropdown.first.click()
            places_page.submit_button_in_kind_modal.click()
            entity_name = kind_name

        with allure.step("Проверить наличие созданного типа в выдаче"):
            places_page.assert_element_name_is_equal(places_page.kind_cards, kind_name)

        with allure.step("Нажать на кнопку редактирования созданного типа"):
            places_page.select_element_by_text(places_page.kind_cards, kind_name).locator(places_page.kind_edit_button).click()

        with allure.step("Изменить название и тип выбранного типа и нажать “Сохранить“"):
            places_page.kind_name_field_in_modal.fill(kind_name_edited)
            places_page.kinds_dropdown_in_modal.click()
            places_page.kinds_options_in_dropdown.last.click()
            places_page.submit_button_in_kind_modal.click()
            entity_name = kind_name_edited

        with allure.step("Проверить наличие измененного типа в выдаче"):
            places_page.assert_element_name_is_equal(places_page.kind_cards, kind_name_edited)

        with allure.step("Нажать на кнопку удаления созданного типа"):
            places_page.select_element_by_text(places_page.kind_cards, kind_name_edited).locator(places_page.kind_delete_button).click()

        with allure.step("Нажать “Подтвердить“"):
            places_page.confirm_delete_button.click()

        with allure.step("Проверить, что удаленный тип не отображается в выдаче"):
            places_page.assert_element_not_present_by_text(places_page.kind_cards, kind_name_edited)

    except Exception:
        if entity_name is not None:
            places_page.open()
            places_page.tab_kinds.click()
            places_page.select_element_by_text(places_page.kind_cards, entity_name).locator(
                places_page.kind_delete_button).click()
            places_page.confirm_delete_button.click()
        raise
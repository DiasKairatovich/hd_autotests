import pytest
import allure
import json
from datetime import datetime, timezone
from core.helpers.cleanup import delete_with_retry, delete_with_retry_by_name
from core.ui.pages.cameras_page import CamerasPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.events_page import EventsPage
from core.ui.pages.groups_page import GroupsPage
from core.ui.pages.lists_page import ListsPage
from core.ui.pages.login_page import LoginPage
from core.ui.pages.map_page import MapPage
from core.ui.pages.places_page import PlacesPage
from core.ui.pages.sensors_page import SensorsPage
from core.ui.pages.subscriptions_page import SubscriptionsPage
from core.ui.pages.users_page import UsersPage
from core.ui.pages.videowalls_page import VideowallsPage
from core.ui.pages.webhooks_page import WebhooksPage
from tests.ui import data


# Включаем запись трейса Playwright и прикладываем в Allure
@pytest.fixture(autouse=True)
def _trace(context, request, tmp_path_factory):
    # Включаем трейс на каждый тест
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    # Сохраняем и прикладываем к отчёту
    path = tmp_path_factory.mktemp("traces") / f"{request.node.name}.zip"
    try:
        context.tracing.stop(path=path)
        allure.attach.file(str(path), name=f"trace-{request.node.name}", attachment_type=allure.attachment_type.ZIP)
    except Exception:
        # если контекст уже закрыт — просто игнорируем
        pass

@pytest.fixture
def auth(page, settings, api_client):
    payload = data.get_token_body
    payload['username'] = settings.username
    payload['password'] = settings.password
    token = api_client.get_token(payload)
    assert token.status_code == 200, f"Token creation failed: {token.json()}"
    token_data = {
        "accessToken": token.json()['access_token'],
        "tokenType": "Bearer",
        "expiresIn": 1800,
        "issuedAt": (datetime.now(timezone.utc)).isoformat(timespec="milliseconds"),
    }

    page.add_init_script(
        script=f'localStorage.setItem("token", JSON.stringify({json.dumps(token_data)}));'
    )
    yield
    payload = data.revoke_token_body
    payload['token'] = token.json()['refresh_token']
    delete_with_retry(
        api_client.revoke_token,
        payload
    )

@pytest.fixture
def login_page(page, settings):
    lp = LoginPage(page,settings)
    lp.open()
    return lp

@pytest.fixture
def dashboard_page(page, settings):
    dashboard_page = DashboardPage(page, settings)
    return dashboard_page

@pytest.fixture
def cameras_page(page, settings):
    cameras_page = CamerasPage(page, settings)
    return cameras_page

@pytest.fixture
def videowalls_page(page, settings):
    videowalls_page = VideowallsPage(page, settings)
    return videowalls_page

@pytest.fixture
def places_page(page, settings):
    places_page = PlacesPage(page, settings)
    return places_page

@pytest.fixture
def lists_page(page, settings):
    lists_page = ListsPage(page, settings)
    return lists_page

@pytest.fixture
def groups_page(page, settings):
    groups_page = GroupsPage(page, settings)
    return groups_page

@pytest.fixture
def users_page(page, settings):
    users_page = UsersPage(page, settings)
    return users_page

@pytest.fixture
def sensors_page(page, settings):
    sensors_page = SensorsPage(page, settings)
    return sensors_page

@pytest.fixture
def subscriptions_page(page, settings):
    subscriptions_page = SubscriptionsPage(page, settings)
    return subscriptions_page

@pytest.fixture
def webhooks_page(page, settings):
    webhooks_page = WebhooksPage(page, settings)
    return webhooks_page

@pytest.fixture
def map_page(page, settings):
    map_page = MapPage(page, settings)
    return map_page

@pytest.fixture
def events_page(page, settings):
    events_page = EventsPage(page, settings)
    return events_page

@pytest.fixture
def videowall(videowalls_page, settings, api_client):
    videowall_name = data.videowall_data()['name']
    try:
        videowalls_page.open()
        videowalls_page.create_new_videowall(videowall_name, settings.username)
        yield videowall_name
    finally:
        delete_with_retry_by_name(
            api_client.search_videowalls,
            api_client.delete_videowall,
            videowall_name
        )

@pytest.fixture
def group(api_client):
    payload = data.group_data()
    group = api_client.create_group(body=payload)

    try:
        assert group.status_code == 200, (
            f"Group creation failed: {group.json()}"
        )
        yield group

    finally:
        group_id = group.json().get('id')

        if group_id:
            delete_with_retry(
                api_client.delete_group,
                group_id
            )
        else:
            delete_with_retry_by_name(
                api_client.search_groups,
                api_client.delete_group,
                payload.get('name')
            )


@pytest.fixture
def place(api_client, group):
    payload = data.place_data(group_ids=[group.json().get('id')])
    place = api_client.create_place(body=payload)

    try:
        assert place.status_code == 200, (
            f"Place creation failed: {place.json()}"
        )
        yield place

    finally:
        place_id = place.json().get('id')

        if place_id:
            delete_with_retry(
                api_client.delete_place,
                place_id
            )
        else:
            delete_with_retry_by_name(
                api_client.search_places,
                api_client.delete_place,
                payload.get('name')
            )


@pytest.fixture
def camera(api_client, place):
    payload = data.camera_data(place_id=place.json().get('id'))
    camera = api_client.create_camera(body=payload)

    try:
        assert camera.status_code == 200, (
            f"Camera creation failed: {camera.json()}"
        )
        yield camera

    finally:
        camera_id = camera.json().get('id')

        if camera_id:
            delete_with_retry(
                api_client.delete_camera,
                camera_id
            )
        else:
            delete_with_retry_by_name(
                api_client.search_cameras,
                api_client.delete_camera,
                payload.get('name')
            )


@pytest.fixture
def cameras_grid(api_client, place):
    created_cameras = []
    failed_payload = None
    failed_response = None

    try:
        for _ in range(21):
            payload = data.camera_data(
                place_id=place.json().get('id')
            )

            response = api_client.create_camera(body=payload)

            if response.status_code != 200:
                failed_payload = payload
                failed_response = response
                break

            camera_id = response.json().get('id')

            if camera_id:
                created_cameras.append(camera_id)

        if failed_response:
            assert failed_response.status_code == 200, (
                f"Camera creation failed: {failed_response.json()}"
            )

        yield

    finally:
        for camera_id in created_cameras:
            delete_with_retry(
                api_client.delete_camera,
                camera_id
            )

        if failed_payload:
            delete_with_retry_by_name(
                api_client.search_cameras,
                api_client.delete_camera,
                failed_payload.get('name')
            )


@pytest.fixture
def subscription(api_client, camera):
    payload = data.subscription_data(
        camera_id=camera.json().get('id'),
        place_id=camera.json().get('place_id')
    )

    subscription = api_client.create_subscription(body=payload)

    try:
        assert subscription.status_code == 200, (
            f"Subscription creation failed: {subscription.json()}"
        )
        yield subscription

    finally:
        subscription_id = subscription.json().get('id')

        if subscription_id:
            delete_with_retry(
                api_client.delete_subscription,
                subscription_id
            )
        else:
            response = api_client.get_subscriptions()

            subscription_id = next(
                (
                    subscription.get("id")
                    for subscription in response.json().get("subscriptions", [])
                    if subscription.get("name") == payload.get("name")
                ),
                None
            )

            if subscription_id:
                delete_with_retry(
                    api_client.delete_subscription,
                    subscription_id
                )
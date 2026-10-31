from uuid import uuid4


def generate_name(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


def camera_data(**overrides):
    data = {
        "name": generate_name("UI_camera"),
        "place_id": "",
        "capacitygroup_token": "0000000000000000",
        "source": {
            "url": "rtsp://10.1.0.23:80/1",
            "body": {
                "protocol": "rtsp",
                "host": "10.1.0.23",
                "port": 80,
                "username": "",
                "password": "",
                "path": "/1",
                "transport": "tcp"
            }
        },
        "video_analytics": {
            "version": 5,
            "modules": [
                {
                    "module": "FaceRecognitionModule",
                    "config": {
                        "min_detection_size": 0.03,
                        "roi": [],
                        "lines": []
                    }
                }
            ]
        }
    }
    data.update(overrides)
    return data

TEST_FILTER_DATA = {
    "fr": "FaceRecognitionModule",
    "ao": "AbandonedObjectsModule"
}

def videowall_data(**overrides):
    data = {
        "name": generate_name("UI_videowall"),
        "grid_layout": [[None] * 16],
        "grid_type": "type1"
    }
    data.update(overrides)
    return data

def place_data(**overrides):
    data = {
        "name": generate_name("UI_place"),
        "latitude": 49.89,
        "longitude": 73.21,
        "group_ids": []
    }
    data.update(overrides)
    return data

def category_data(**overrides):
    data = {
        "name": generate_name("UI_placecategory"),
    }
    data.update(overrides)
    return data

def kind_data(**overrides):
    data = {
        "name":generate_name("UI_placekind"),
        "icon":"courtyard"
    }
    data.update(overrides)
    return data

def list_data(**overrides):
    data = {
        "name":generate_name("UI_list"),
        "description":"",
        "priority":"low",
        "threshold":"medium",
        "activity_tracking":False,
        "group_ids":[]
    }
    data.update(overrides)
    return data

def group_data(**overrides):
    data = {
        "name": generate_name("UI_group"),
        "description": "Autotest group",
    }
    data.update(overrides)
    return data

def user_data(**overrides):
    max_length  = 25
    data = {
        "name": generate_name("UI_user")[:max_length],
        "last_name": generate_name("UI_user_lastname")[:max_length],
        "email": generate_name("UI_user_mail")[:max_length] + "@teye.dev",
    }
    data.update(overrides)
    return data

def sensor_data(**overrides):
    data = {
        "kind":"testident",
        "name":generate_name("UI_sensor"),
        "place_id": None
    }
    data.update(overrides)
    return data


def subscription_data(**overrides):
    data = {
        "name": generate_name("UI_subscription"),
        "kind": "event",
        "event_type": "sa",
        "event_reason": 1,
        "match_kind": "all",
        "place_id": None,
        "camera_id": "",
        "config": {
            "worktime": [
                [True] * 24,
                [True] * 24,
                [True] * 24,
                [True] * 24,
                [True] * 24,
                [True] * 24,
                [True] * 24,
            ],
            "store": False
        }
    }
    data.update(overrides)
    return data

def webhook_data(**overrides):
    data = {
        "name": generate_name("UI_webhook"),
        "method": "post",
        "url": "https://example.com/api/v1/example",
        "content_type": "text/plain",
        "tls_verify": False,
        "subscription_id": "",
        "kind": "notification",
        "is_enabled": True
    }
    data.update(overrides)
    return data

def search_data(**overrides):
    data = {
        "query": None,
    }
    data.update(overrides)
    return data

get_token_body = {
    "grant_type": "password",
    "username": "",
    "password": ""
}

revoke_token_body = {
    "token": "",
    "token_type_hint": "refresh_token"
}